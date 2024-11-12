import os
import time

import jieba
import math
import operator
import configparser

from datetime import datetime, timedelta
import jieba.analyse as analyse  # 关键词提取，引入推荐功能

from django.db import connection

from searchApp.config import logger
from searchApp.core.utils import funcUtils

log = logger.createLogger('indexService')


class SearchEngine:
    stop_words = set()

    config_path = ''
    config_encoding = ''

    K1 = 0
    B = 0
    N = 0
    AVG_L = 0

    HOT_K1 = 0
    HOT_K2 = 0

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        # f = open(config['DEFAULT']['stop_words_path'], encoding=config['DEFAULT']['stop_words_encoding'])
        # words = f.read()
        # self.stop_words = set(words.split('\n'))
        # self.conn = sqlite3.connect(config['DEFAULT']['db_path'])
        self.K1 = float(config['DEFAULT']['k1'])
        self.B = float(config['DEFAULT']['b'])
        self.N = int(config['DEFAULT']['n'])
        self.AVG_L = float(config['DEFAULT']['avg_l'])
        # self.HOT_K1 = float(config['DEFAULT']['hot_k1'])
        # self.HOT_K2 = float(config['DEFAULT']['hot_k2'])

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

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

    def fetch_from_db(self, term):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM index_article WHERE term=%s', (term,))
        return cursor.fetchone()

    def result_by_BM25(self, seg_list, from_time):
        n, cleaned_dict = self.clean_list(seg_list)
        BM25_scores = {}
        cur_time = datetime.now()
        for term in cleaned_dict.keys():
            r = self.fetch_from_db(term)
            if r is None:
                continue
            df = r[2]
            w = math.log2((self.N - df + 0.5) / (df + 0.5))
            docs = r[3].split('\n')
            for doc in docs:
                docid, date_time, tf, ld = doc.split('\t')
                docid = str(docid)
                date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                tf = int(tf)
                ld = int(ld)
                if from_time == 'all' or (from_time == 'day' and cur_time - date_time <= timedelta(days=1)) or (
                        from_time == 'week' and cur_time - date_time <= timedelta(days=7)) or (
                        from_time == 'month' and cur_time - date_time <= timedelta(days=30)):
                    s = (self.K1 * tf * w) / (tf + self.K1 * (1 - self.B + self.B * ld / self.AVG_L))
                    if docid in BM25_scores:
                        BM25_scores[docid] = BM25_scores[docid] + s
                    else:
                        BM25_scores[docid] = s
        BM25_scores = sorted(BM25_scores.items(), key=operator.itemgetter(1))
        BM25_scores.reverse()
        if len(BM25_scores) == 0:
            return 0, []
        else:
            return 1, BM25_scores

    def getResultByBM25(self, pendingList, fromTime):
        """
        根据划分好的数据获取搜索结果
        :param pendingList: 传入的list
        :param fromTime: 日期起始
        :return:
        """
        n, cleanDict = self.clean_list(pendingList)  # 对数据进行净化
        BM25_scores = {}
        cur_time = datetime.now()
        for key in cleanDict.keys():
            r = self.fetch_from_db(key)
            if r is None:
                continue
            df = r[2]
            w = math.log2((self.N - df + 0.5) / (df + 0.5))
            docs = r[3].split('\n')
            for doc in docs:
                docid, date_time, tf, ld = doc.split('\t')
                docid = str(docid)
                date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                tf = int(tf)
                ld = int(ld)
                if fromTime == 'all' or (fromTime == 'day' and cur_time - date_time <= timedelta(days=1)) or (
                        fromTime == 'week' and cur_time - date_time <= timedelta(days=7)) or (
                        fromTime == 'month' and cur_time - date_time <= timedelta(days=30)):
                    s = (self.K1 * tf * w) / (tf + self.K1 * (1 - self.B + self.B * ld / self.AVG_L))
                    if docid in BM25_scores:
                        BM25_scores[docid] = BM25_scores[docid] + s
                    else:
                        BM25_scores[docid] = s
        BM25_scores = sorted(BM25_scores.items(), key=operator.itemgetter(1))
        BM25_scores.reverse()
        if len(BM25_scores) == 0:
            return 0, []
        else:
            return 1, BM25_scores

    def search(self, seg_list, fromtime, sort_type=0):
        if sort_type == 0:
            return self.result_by_BM25(seg_list, fromtime)


def getAll(content, from_time='all'):
    se = SearchEngine(os.path.abspath('./searchApp/config/config.ini'), 'utf-8')
    seg_list = jieba.lcut_for_search(content)
    # seg_list = jieba.lcut(content, cut_all=False)
    log.info('划分结果为：{}'.format(seg_list))
    flag, result = se.search(seg_list, from_time, 0)
    return flag, result, seg_list


def getAll_further(content, from_time='all'):
    se = SearchEngine(os.path.abspath('./searchApp/config/config.ini'), 'utf-8')
    seg_list = list(content)
    log.info('划分结果为：{}'.format(seg_list))
    flag, result = se.search(seg_list, from_time, 0)
    return flag, result, seg_list


def getPart(content, num):
    se = SearchEngine(os.path.abspath('./searchApp/config/config.ini'), 'utf-8')
    flag, result = se.search(content, 'all', 0)
    return flag, result[:num]


def getData(searchMap):
    """
    根据传入的关键词查找sql
    :param searchMap:
    :return: 内容、总条数、查询时间、总页码、页码、页码大小
    """
    start = time.clock()
    searchContent = searchMap.get('searchContent')
    searchTime = searchMap.get('searchTime')
    searchPage = searchMap.get('searchPage')
    pageSize = 10
    params = []

    sql = "select article.id, article.title, left(article.content, 500) as content, article.publishtime, " \
          "article.pic, sourcesite.icon, sourcesite.name, articletype.name as typename " \
          "from article " \
          "left join sourcesite on article.source = sourcesite.id " \
          "left join articletype on article.type = articletype.id " \
          "where article.state_isenabled = '1' and sourcesite.state_isenabled = '1' "

    # allData是已经按照相关度排序的，按照页码进行处理
    flag, allData, tags = getAll(searchContent, searchTime)
    if flag == 0:
        log.error('jieba分词查询模式失败，将转换为字符串分割模式')
        flag, allData, tags = getAll_further(searchContent, searchTime)
        if flag == 0:
            log.error('字符串分割模式查询失败，将返回空结果')
            sql += " and 1 = 0 "

    count = len(allData)
    pageCount = int(count / pageSize) if count % pageSize == 0 else int(count / pageSize) + 1
    if searchPage > pageCount:
        searchPage = pageCount
    retData = allData[(searchPage - 1) * 10: searchPage * 10]
    if len(retData) != 0:
        sql += "and article.id in (" + ','.join(['%s'] * len(retData)) + ") "
        for data in retData:
            params.append(data[0])
        # 结果排序处理
        sql += "order by field(article.id," + ','.join(['%s'] * len(retData)) + ") "
        for data in retData:
            params.append(data[0])

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]

    rowNumber = 0
    for rs in result:
        rs['rownumber'] = rowNumber
        rowNumber += 1

    end = time.clock()

    return {'news': result,
            'count': count,
            'time': round(end - start, 4),
            'pagecount': pageCount,
            'pagesize': pageSize,
            'page': searchPage,
            'sc': searchContent,
            'st': searchTime,
            }


def getRecommendData(searchContent):
    """
    推荐阅读
    :param searchContent:
    :return:
    """
    extract = analyse.extract_tags(searchContent, 1)
    if len(extract) != 1:
        return {'data': False}
    key_content = [extract[0]]
    log.info('关键词划分为：{}'.format(key_content))
    if key_content[0] == searchContent:
        return {'data': False}
    else:
        flag, retData = getPart(key_content, 10)
        if flag == 0:
            return {'data': False}
        else:
            if len(retData) != 0:
                sql = "select id, title, date_format(publishtime, '%%Y-%%m-%%d') = date(now()) as istoday from article " \
                      "where id in (" + ','.join(['%s'] * len(retData)) + ") "
                params = []
                for data in retData:
                    params.append(data[0])
                # 结果排序处理
                sql += "order by field(id," + ','.join(['%s'] * len(retData)) + ") "
                for data in retData:
                    params.append(data[0])
                with connection.cursor() as cursor:
                    cursor.execute(sql, params)
                    description = cursor.description
                    result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
                return {'data': True, 'result': result}
            else:
                return {'data': False}


def getRecommendDataByArticle(curId):
    """
    推荐阅读
    :param curId:
    :return:
    """
    title = funcUtils.getNewsTitleById(curId)
    key_content = jieba.lcut_for_search(title)
    log.info('关键词划分为：{}'.format(key_content))
    flag, retData = getPart(key_content, 4)
    if flag == 0:
        return {'data': False}
    else:
        if len(retData) != 0:
            sql = "select id, title, publishtime, date_format(publishtime, '%%Y-%%m-%%d') = date(now()) as istoday from article " \
                  "where id in (" + ','.join(['%s'] * len(retData)) + ") and id <> %s "
            params = []
            for data in retData:
                params.append(data[0])
            params.append(curId)
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                description = cursor.description
                result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
            return {'data': True, 'result': result}
        else:
            return {'data': False}
