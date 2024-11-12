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
log = logger.createLogger("sinaNewsService")

global source, creator


def crawler(pageNum, userName):
    """
    爬虫主函数
    :param userName:
    :param pageNum: 需求页码，正常情况下每页包含50条新闻
    :return:
    """
    try:
        start = time.clock()

        # 判断来源是否有效
        global source, creator
        source = funcUtils.getSourceByName('新浪网')
        if source is None:
            log.error('获取新闻来源信息错误，请检查预置数据表，参数：新浪网')
            raise ValueError('获取新闻来源信息错误，请检查预置数据表，参数：新浪网')
        log.info("正在获取新浪网[https://news.sina.com.cn/]数据，入参：{}".format(pageNum))
        creator = userName

        successInfo = []

        lid = [2510, 2511, 2512, 2513, 2514, 2515, 2516, 2669]
        lidDict = {2510: '国内', 2511: '国际', 2512: '体育', 2513: '娱乐', 2514: '军事', 2515: '科技', 2516: '财经',
                   2669: '社会'}

        for pageType in lid:
            # 判断类型是否有效
            curType = funcUtils.getTypeByName(lidDict.get(pageType))
            if curType is None:
                log.error(
                    '获取新闻类型信息出错，请检查预置数据表，将跳过此条数据，参数：{}'.format(lidDict[pageType]))
                continue

            for page in range(1, int(pageNum)):
                """
                lid: 2509全部 2510国内 2511国际 2669社会 2512体育 2513娱乐 2514军事 2515科技 2516财经
                """
                url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}'.format(pageType,
                                                                                                             page)
                try:
                    response = requests.get(url)
                    if response.status_code != 200:
                        raise ValueError('url状态码异常，状态码为{}，参数：{}'.format(response.status_code, url))
                except Exception as e:
                    log.error('参数为{}的数据存在异常，将跳过，请注意检查：{}'.format(page, e))
                    continue
                response.encoding = 'utf-8'
                soup = bs(response.text, 'html.parser')
                jd = json.loads(soup.text)
                for info in jd['result']['data']:
                    # url内容转dict
                    newsResult = getUrlInfo(info['url'])
                    if newsResult is None:
                        continue

                    # 补充其他信息
                    newsResult['source'] = source
                    newsResult['type'] = curType

                    successInfo.append(newsResult)

        successCount = writeIntoDatabase(successInfo)  # 集中加入数据库
        end = time.clock()
        PatchLog.objects.create(
            id=uuid.uuid4(),
            type='Update',
            info='数据库更新完成，新增{}条数据：新浪网，用时{}分'.format(successCount, round((end - start) / 60, 4)),
            patchtime=datetime.now(),
            creator=creator
        )
        log.info('新浪网[https://news.sina.com.cn/]数据更新完成，数量：{}'.format(successCount))
        return True
    except Exception as e:
        traceback.print_exc()
        PatchLog.objects.create(
            id=uuid.uuid4(),
            type='UpdateError',
            info='数据库更新失败：新浪网，{}'.format(e),
            patchtime=datetime.now(),
            creator=creator
        )
        log.error('新浪网[https://news.sina.com.cn/]数据更新失败，{}'.format(e))
        return False


def getUrlInfo(url):
    """
    根据每条新闻的url信息去获取正文
    :param url: url信息
    :return: 正文
    """
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        soup = bs(response.text, 'html.parser')

        try:
            title = soup.select('.main-title')[0].text

            date = soup.select('.date')[0].text
            publishTime = datetime.strptime(date, '%Y年%m月%d日 %H:%M')

            content = soup.select('.article p')[:-1]
            content = '\n\t'.join([p.text.strip() for p in content])  # 将文章中的每一段用\n\t隔开
            content = '\t' + content
        except:
            log.error('遇到了元素缺少错误，请升级系统后再次尝试')
            return

        pic = soup.select('.img_wrapper')
        if pic:
            try:
                picUrl = pic[0].next.attrs['src']
            except:
                picUrl = None
        else:
            picUrl = None

        keyExist = soup.select('.keywords')
        if keyExist:
            try:
                keyList = keyExist[0].contents
                keywords = ''
                keywordsFlag = False  # 用于剔除关键字起始
                for keyword in keyList:
                    if hasattr(keyword, 'text'):
                        if keywordsFlag:
                            keywords += keyword.text
                            keywords += ' '
                        keywordsFlag = True
                keywords = keywords.strip()
            except:
                keywords = None
        else:
            keywords = None

        result = {
            'tags': keywords,
            'title': title,
            'content': content,
            'pic': picUrl,
            'url': url,
            'publishtime': publishTime
        }

        return result
    else:
        log.error('url状态码异常，状态码为{}，参数：{}'.format(response.status_code, url))
        return


@transaction.atomic
def writeIntoDatabase(info):
    """
    写入数据库
    :param info:
    :return:
    """
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
