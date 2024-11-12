import json  # 处理json格式的数据
import time
import traceback
import uuid
from datetime import datetime

import requests  # 用于发起请求，获取网页信息
from bs4 import BeautifulSoup as bs  # 用于数据抽取
from django.db import transaction

from searchApp.config import logger
from searchApp.core.utils import funcUtils
from searchApp.models import Article, PatchLog

# create logger
log = logger.createLogger("cctvNewsService")

global source, creator


def crawler(pageNum, userName):
    """
    暂时只接入国内、国际、社会、科技、娱乐
    :param pageNum:
    :param userName:
    :return:
    """
    try:
        start = time.clock()

        global source, creator
        source = funcUtils.getSourceByName('央视网')
        if source is None:
            log.error('获取新闻来源信息错误，请检查预置数据表，参数：央视网')
            raise ValueError('获取新闻来源信息错误，请检查预置数据表，参数：央视网')
        pageNum = funcUtils.pageParamToInt(pageNum)
        log.info("正在获取央视网[https://news.cctv.com/]数据，入参：{}".format(pageNum))
        creator = userName

        successInfo = []

        lid = ['china', 'world', 'society', 'ent', 'tech']
        typeDict = {'china': '国内', 'world': '国际', 'society': '社会', 'ent': '娱乐', 'tech': '科技'}

        for pageType in lid:
            curType = funcUtils.getTypeByName(typeDict.get(pageType))
            if curType is None:
                log.error(
                    '获取新闻类型信息出错，请检查预置数据表，将跳过此条数据，参数：{}'.format(typeDict[pageType]))
                continue

            for page in range(1, int(pageNum)):
                url = 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/{}_{}.jsonp?cb={}'.format(pageType,
                                                                                                            page,
                                                                                                            pageType)
                try:
                    response = requests.get(url)
                    if response.status_code != 200:
                        raise ValueError('url状态码异常，状态码为{}，参数：{}'.format(response.status_code, url))
                except Exception as e:
                    log.error('参数为{}的数据存在异常，将跳过，请注意检查：{}'.format(page, e))
                    continue

                response.encoding = 'utf-8'
                resText = response.text
                jd = json.loads(resText.replace(pageType + '(', '').replace(resText[-1], ''))
                for info in jd['data']['list']:
                    newsResult = getUrlInfo(info)
                    if newsResult is None:
                        continue
                    newsResult['source'] = source
                    newsResult['type'] = curType

                    successInfo.append(newsResult)

        successCount = writeIntoDatabase(successInfo)  # 集中加入数据库
        end = time.clock()
        PatchLog.objects.create(
            id=uuid.uuid4(),
            type='Update',
            info='数据库更新完成，新增{}条数据：央视网，用时{}分'.format(successCount, round((end - start) / 60, 4)),
            patchtime=datetime.now(),
            creator=creator
        )
        log.info('央视网[https://news.cctv.com/]数据更新完成，数量：{}'.format(successCount))
        return True
    except Exception as e:
        traceback.print_exc()
        PatchLog.objects.create(
            id=uuid.uuid4(),
            type='UpdateError',
            info='数据库更新失败：央视网，{}'.format(e),
            patchtime=datetime.now(),
            creator=creator
        )
        log.error('央视网[https://news.cctv.com/]数据更新失败，{}'.format(e))
        return False


def getUrlInfo(info):
    response = requests.get(info['url'])
    response.encoding = 'utf-8'
    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')

        try:
            title = info['title']

            publishTime = datetime.strptime(info['focus_date'], '%Y-%m-%d %H:%M:%S')

            content = soup.select('.content_area p')
            content = '\n\t'.join([p.text.strip() for p in content])  # 将文章中的每一段用\n\t隔开
            content = '\t' + content

            pic = info['image'] if info['image'] != '' else None

            if len(info['keywords']) != 0:
                tags = info['keywords']
            else:
                tags = None

        except:
            log.error('遇到了元素缺少错误，请升级系统后再次尝试')
            return

        result = {
            'tags': tags,
            'title': title,
            'content': content,
            'pic': pic,
            'url': info['url'],
            'publishtime': publishTime
        }
        return result

    else:
        log.error('url状态码异常，状态码为{}，参数：{}'.format(response.status_code, info['url']))
        return


@transaction.atomic
def writeIntoDatabase(info):
    with transaction.atomic():
        successCount = 0
        for i in info:
            try:
                # 先检查该url是否已存在，存在则跳过
                if funcUtils.ifArticleNotExist(i['url']):
                    Article.objects.create(
                        id=uuid.uuid4(),
                        type=i['type'],
                        source=i['source'],
                        tags=i['tags'],
                        title=i['title'],
                        content=i['content'],
                        pic=i['pic'],
                        url=i['url'],
                        publishtime=i['publishtime'],
                        pageview=0,
                        state_isenabled=1,
                        timestamp_createdby=creator,
                        timestamp_createdon=datetime.now(),
                        timestamp_lastchangedby=creator,
                        timestamp_lastchangedon=datetime.now()
                    )
                    successCount += 1
            except Exception as e:
                log.error('数据库更新失败，详情如下：')
                traceback.print_exc()
    return successCount
