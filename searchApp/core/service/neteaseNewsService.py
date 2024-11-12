import time
import traceback
import uuid

import requests
from bs4 import BeautifulSoup as bs  # 用于数据抽取
from datetime import datetime

from django.db import transaction

from searchApp.config import logger
from searchApp.core.utils import funcUtils
from searchApp.models import PatchLog, Article

log = logger.createLogger("neteaseNewsService")

global source, creator


def crawler(pageNum, userName):
    """
    爬虫主函数，每页含有70条，默认爬取6页，420*8=3360
    :param pageNum: 最大为8
    :param userName:
    :return:
    """
    # 最大为08
    try:
        start = time.clock()

        global source, creator
        source = funcUtils.getSourceByName('网易新闻')
        if source is None:
            log.error('获取新闻来源信息错误，请检查预置数据表，参数：网易新闻')
            raise ValueError('获取新闻来源信息错误，请检查预置数据表，参数：网易新闻')
        pageNum = funcUtils.pageParamToInt(pageNum)
        if pageNum > 9:
            pageNum = 9
        log.info("正在获取网易新闻[https://news.163.com/]数据，入参：{}".format(pageNum))
        creator = userName

        successInfo = []

        lid = ['guonei', 'guoji', 'war', 'tech', 'money', 'sports', 'ent', 'shehui']
        typeDict = {'guonei': '国内', 'guoji': '国际', 'war': '军事', 'tech': '科技', 'money': '财经', 'sports': '体育',
                    'ent': '娱乐', 'shehui': '社会'}

        for pageType in lid:
            curType = funcUtils.getTypeByName(typeDict.get(pageType))
            if curType is None:
                log.error(
                    '获取新闻类型信息出错，请检查预置数据表，将跳过此条数据，参数：{}'.format(typeDict[pageType]))
                continue

            for page in range(1, pageNum):
                if page == 1:
                    url = 'https://temp.163.com/special/00804KVA/cm_{}.js?callback=data_callback'.format(pageType)
                else:
                    url = 'https://temp.163.com/special/00804KVA/cm_{}_0{}.js?callback=data_callback'.format(pageType,
                                                                                                             page)
                try:
                    headers = {
                        "Host": "temp.163.com",
                        "Connection": "keep-alive",
                        "Accept": "*/*",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
                        "Referer": "http://news.163.com/",
                        "Accept-Encoding": "gzip, deflate, sdch",
                        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                    }
                    response = requests.get(url=url, headers=headers)
                    if response.status_code != 200:
                        raise ValueError('url状态码异常，状态码为{}，参数：{}'.format(response.status_code, url))
                except Exception as e:
                    log.error('参数为{}的数据存在异常，将跳过，请注意检查：{}'.format(page, e))
                    continue

                resData = response.text
                data = eval(resData.replace('data_callback(', '').replace(resData[-1], ""))
                for info in data:
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
            info='数据库更新完成，新增{}条数据：网易新闻，用时{}分'.format(successCount, round((end - start) / 60, 4)),
            patchtime=datetime.now(),
            creator=creator
        )
        log.info('网易新闻[https://news.163.com/]数据更新完成，数量：{}'.format(successCount))
        return True
    except Exception as e:
        traceback.print_exc()
        PatchLog.objects.create(
            id=uuid.uuid4(),
            type='UpdateError',
            info='数据库更新失败：网易新闻，{}'.format(e),
            patchtime=datetime.now(),
            creator=creator
        )
        log.error('网易新闻[https://news.163.com/]数据更新失败，{}'.format(e))
        return False


def getUrlInfo(info):
    """
    根据url信息获取新闻内容
    :param info:
    :return:
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
    }
    response = requests.get(url=info['docurl'], headers=headers)
    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')

        try:
            title = info['title']

            publishTime = datetime.strptime(info['time'], '%m/%d/%Y %H:%M:%S')

            content = soup.select('.post_body p')
            content = '\n\t'.join([p.text.strip() for p in content])  # 将文章中的每一段用\n\t隔开
            content = '\t' + content

            pic = info['imgurl'] if info['imgurl'] != '' else None

            tags = ''
            if len(info['keywords']) != 0:
                for keyword in info['keywords']:
                    tags += keyword.get('keyname')
                    tags += ' '
                tags = tags.strip()
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
            'url': info['docurl'],
            'publishtime': publishTime
        }
        return result

    else:
        log.error('url状态码异常，状态码为{}，参数：{}'.format(response.status_code, info['docurl']))
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
