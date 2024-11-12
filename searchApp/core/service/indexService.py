import os
import time
import traceback
import uuid

import jieba
import configparser

from django.db import connection
from datetime import datetime, timedelta

from searchApp.config import logger
from searchApp.models import PatchLog

log = logger.createLogger('indexService')


class Doc:
    docId = 0
    date_time = ''
    tf = 0
    ld = 0

    def __init__(self, docId, date_time, tf, ld):
        self.docId = docId
        self.date_time = date_time
        self.tf = tf
        self.ld = ld

    def __repr__(self):
        return str(self.docId) + '\t' + self.date_time + '\t' + str(self.tf) + '\t' + str(self.ld)


class IndexModule:
    stop_words = set()
    postings_lists = {}

    config_path = ''
    config_encoding = ''

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)

    def clean_list(self, seg_list):
        cleaned_dict = {}
        n = 0
        for i in seg_list:
            i = i.strip().lower()
            if i != '':
                n = n + 1
                if i in cleaned_dict:
                    cleaned_dict[i] = cleaned_dict[i] + 1
                else:
                    cleaned_dict[i] = 1
        return n, cleaned_dict

    def write_index_to_db(self):
        # try:
        with connection.cursor() as cursor:
            cursor.execute('delete from index_article')
            for key, value in self.postings_lists.items():
                doc_list = '\n'.join(map(str, value[1]))
                t = (uuid.uuid4(), key, value[0], doc_list)
                cursor.execute('insert into index_article value(%s, %s, %s, %s)', t)

    def construct_postings_lists(self):
        config = configparser.ConfigParser()
        config.read(self.config_path, self.config_encoding)
        with connection.cursor() as cursor:
            sql = "select id, title, left(content, 100) as content, publishtime from article "
            cursor.execute(sql)
            description = cursor.description
            files = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
        AVG_L = 0
        for i in files:
            title = i['title']
            docId = i['id']
            date_time = i['publishtime'].strftime("%Y-%m-%d %H:%M:%S")
            # seg_list = jieba.lcut(title, cut_all=False)
            seg_list = jieba.lcut_for_search(title)

            ld, cleaned_dict = self.clean_list(seg_list)

            AVG_L = AVG_L + ld

            for key, value in cleaned_dict.items():
                d = Doc(docId, date_time, value, ld)
                if key in self.postings_lists:
                    self.postings_lists[key][0] = self.postings_lists[key][0] + 1  # df++
                    self.postings_lists[key][1].append(d)
                else:
                    self.postings_lists[key] = [1, [d]]  # [df, [Doc]]
        AVG_L = AVG_L / len(files)
        config.set('DEFAULT', 'N', str(len(files)))
        config.set('DEFAULT', 'avg_l', str(AVG_L))
        with open(self.config_path, 'w', encoding=self.config_encoding) as configfile:
            config.write(configfile)
        self.write_index_to_db()


def updateIndex(userName):
    try:
        start = time.clock()
        log.warning('正在构建索引，请不要关闭服务器，否则可能造成数据丢失...')
        im = IndexModule(os.path.abspath('./searchApp/config/config.ini'), 'utf-8')
        im.construct_postings_lists()
        # v1.3新增：将最新新闻插入到var01中
        log.warning('正在构建必要文件，请不要关闭服务器，否则可能造成数据丢失...')
        with connection.cursor() as cursor:
            clearSql = "update article set var01 = null where var01 = '1' "
            cursor.execute(clearSql)
            typeSql = "select id from articletype "
            cursor.execute(typeSql)
            allType = [i[0] for i in cursor.fetchall()]
            newList = []
            for curType in allType:
                sql = "select id from article where type = %s order by publishtime desc limit 10 offset 0 "
                cursor.execute(sql, curType)
                newList.extend([i[0] for i in cursor.fetchall()])
            if len(newList) != 0:
                updateSql = "update article set var01 = '1' where id in (" + ','.join(['%s'] * len(newList)) + ") "
                cursor.execute(updateSql, newList)
        end = time.clock()
        log.info('更新索引完成，用时{}分'.format(round((end - start) / 60, 4)))
        PatchLog.objects.create(
            id=uuid.uuid4(),
            type='Update',
            info='更新索引完成，用时{}分'.format(round((end - start) / 60, 4)),
            patchtime=datetime.now(),
            creator=userName
        )
        return True
    except Exception as e:
        PatchLog.objects.create(
            id=uuid.uuid4(),
            type='UpdateError',
            info='更新索引失败：{}'.format(e),
            patchtime=datetime.now(),
            creator=userName
        )
        log.error('更新索引失败：{}，错误信息如下：'.format(e))
        traceback.print_exc()
        return False


def deleteOldDatas(userName):
    try:
        with connection.cursor() as cursor:
            oldDate = datetime.strftime(datetime.now() + timedelta(days=-90), "%Y-%m-%d 00:00:00")
            sql = 'delete from article where publishtime < %s '
            log.warning('执行【删除】sql：{}，参数：{}'.format(sql, oldDate))
            cursor.execute(sql, oldDate)
            result = cursor.rowcount
            log.info('自{}起旧数据已删除，数量：{}'.format(oldDate, result))
            PatchLog.objects.create(
                id=uuid.uuid4(),
                type='Delete',
                info='自{}起旧数据已删除，数量：{}'.format(oldDate, result),
                patchtime=datetime.now(),
                creator=userName
            )
            return True
    except Exception as e:
        PatchLog.objects.create(
            id=uuid.uuid4(),
            type='DeleteError',
            info='旧数据删除失败：{}'.format(e),
            patchtime=datetime.now(),
            creator=userName
        )
        log.error('旧数据删除失败：{}，错误信息如下：'.format(e))
        traceback.print_exc()
        return False
    finally:
        cursor.close()
