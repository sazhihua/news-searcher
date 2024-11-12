import time
import traceback
import uuid

import requests
from bs4 import BeautifulSoup as bs  # 用于数据抽取
from datetime import datetime, timedelta

from django.db import transaction

from searchApp.config import logger
from searchApp.core.utils import funcUtils
from searchApp.models import PatchLog, Article

log = logger.createLogger("paperNewsService")

global source, creator, curType


def crawler(userName):
    try:
        start = time.clock()

        global source, creator, curType
        source = funcUtils.getSourceByName('人民日报')
        if source is None:
            log.error('获取新闻来源信息错误，请检查预置数据表，参数：人民日报')
            raise ValueError('获取新闻来源信息错误，请检查预置数据表，参数：人民日报')
        creator = userName
        curType = funcUtils.getTypeByName('报纸')
        if source is None:
            log.error('获取新闻类型信息出错，请检查预置数据表，将跳过此条数据，参数：{}'.format('报纸'))
            raise ValueError('获取新闻类型信息出错，请检查预置数据表，将跳过此条数据，参数：{}'.format('报纸'))
        curDate = datetime.now()
        log.info("正在获取人民日报[http://www.people.com.cn/]数据，入参：{}".format(curDate))

        year = str(curDate.year)
        month = '0' + str(curDate.month) if curDate.month < 10 else str(curDate.month)
        day = '0' + str(curDate.day) if curDate.day < 10 else str(curDate.day)
        curDayList = downloadPaper(year, month, day)

        successCount = writeIntoDatabase(curDayList)
        end = time.clock()
        PatchLog.objects.create(
            id=uuid.uuid4(),
            type='Update',
            info='数据库更新完成，新增{}条数据：人民日报，用时{}分'.format(successCount, round((end - start) / 60, 4)),
            patchtime=datetime.now(),
            creator=creator
        )
        log.info('人民日报[http://www.people.com.cn/]数据更新完成，数量：{}'.format(successCount))
        return True
    except Exception as e:
        traceback.print_exc()
        PatchLog.objects.create(
            id=uuid.uuid4(),
            type='UpdateError',
            info='数据库更新失败：人民日报，{}'.format(e),
            patchtime=datetime.now(),
            creator=creator
        )
        log.error('人民日报[http://www.people.com.cn/]数据更新失败，{}'.format(e))
        return False


def fetchUrl(url):
    """
    功能：访问 url 的网页，获取网页内容并返回
        参数：目标网页的 url
        返回：目标网页的 html 内容
    """
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ValueError('url状态码异常，状态码为{}，参数：{}'.format(r.status_code, url))
    r.encoding = r.apparent_encoding
    return r.text


def getPageList(year, month, day):
    """
    功能：获取当天报纸的各版面的链接列表
    参数：年，月，日
    """
    url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/nbs.D110000renmrb_01.htm'
    html = fetchUrl(url)
    bsobj = bs(html, 'html.parser')
    temp = bsobj.find('div', attrs={'id': 'pageList'})
    if temp:
        pageList = temp.ul.find_all('div', attrs={'class': 'right_title-name'})
    else:
        pageList = bsobj.find('div', attrs={'class': 'swiper-container'}).find_all('div',
                                                                                   attrs={'class': 'swiper-slide'})
    linkList = []

    for page in pageList:
        link = page.a["href"]
        url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/' + link
        linkList.append(url)

    return linkList


def getTitleList(year, month, day, pageUrl):
    """
    功能：获取报纸某一版面的文章链接列表
    参数：年，月，日，该版面的链接
    """
    html = fetchUrl(pageUrl)
    bsobj = bs(html, 'html.parser')
    temp = bsobj.find('div', attrs={'id': 'titleList'})
    if temp:
        titleList = temp.ul.find_all('li')
    else:
        titleList = bsobj.find('ul', attrs={'class': 'news-list'}).find_all('li')
    linkList = []

    for title in titleList:
        tempList = title.find_all('a')
        for temp in tempList:
            link = temp["href"]
            if 'nw.D110000renmrb' in link:
                url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/' + link
                linkList.append(url)

    return linkList


def getContent(html, temp):
    """
    功能：解析 HTML 网页，获取新闻的文章内容
    参数：html 网页内容
    """

    bsobj = bs(html, 'html.parser')

    # 获取文章 标题
    title = (bsobj.h3.text + ' ' + bsobj.h1.text + ' ' + bsobj.h2.text).strip()
    # print(title)

    # 获取文章 内容
    content = bsobj.find('div', attrs={'id': 'ozoom'}).find_all('p')
    content = '\n\t'.join([p.text.strip() for p in content])  # 将文章中的每一段用\n\t隔开
    content = '\t' + content
    # for p in pList:
    #     content += p.text + '\n'
    #     # print(content)

    # 获取其他内容
    picUrl = bsobj.select('.pci_c img')
    if len(picUrl) != 0:
        pic = 'http://paper.people.com.cn/rmrb/' + picUrl[0].attrs['src'][9:]
    else:
        pic = None

    temp['title'] = title
    temp['content'] = content
    temp['pic'] = pic

    return temp


def downloadPaper(year, month, day):
    """
    功能：爬取《人民日报》网站 某年 某月 某日 的新闻内容，并保存在 指定目录下
    参数：年，月，日，文件保存的根目录
    """
    curDayList = []
    pageList = getPageList(year, month, day)
    for page in pageList:
        titleList = getTitleList(year, month, day, page)
        for url in titleList:
            # 暂时存储数据
            temp = {
                'url': url,
                'publishtime': datetime(int(year), int(month), int(day), 8, 0, 0),
            }
            # 获取新闻文章内容
            html = fetchUrl(url)
            info = getContent(html, temp)

            curDayList.append(info)
    return curDayList


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
                        type=curType,
                        source=source,
                        tags=None,
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


# def crawler(userName):
#     try:
#         days = 0
#         curDate = datetime.now() + timedelta(days=-60)
#         while days != 30:
#             global source, creator, curType
#             source = funcUtils.getSourceByName('人民日报')
#             if source is None:
#                 log.error('获取新闻来源信息错误，请检查预置数据表，参数：人民日报')
#                 raise ValueError('获取新闻来源信息错误，请检查预置数据表，参数：人民日报')
#             creator = userName
#             curType = funcUtils.getTypeByName('报纸')
#             if source is None:
#                 log.error('获取新闻类型信息出错，请检查预置数据表，将跳过此条数据，参数：{}'.format('报纸'))
#                 raise ValueError('获取新闻类型信息出错，请检查预置数据表，将跳过此条数据，参数：{}'.format('报纸'))
#             log.info("正在获取人民日报[http://www.people.com.cn/]数据，入参：{}".format(curDate))
#
#             year = str(curDate.year)
#             month = '0' + str(curDate.month) if curDate.month < 10 else str(curDate.month)
#             day = '0' + str(curDate.day) if curDate.day < 10 else str(curDate.day)
#             curDayList = downloadPaper(year, month, day)
#             writeIntoDatabase(curDayList)
#
#             log.info('人民日报[http://www.people.com.cn/]数据更新完成' + str(days))
#             curDate = curDate + timedelta(days=-1)
#             days += 1
#         return True
#     except Exception as e:
#         traceback.print_exc()
#         PatchLog.objects.create(
#             id=uuid.uuid4(),
#             type='UpdateError',
#             info='数据库更新失败：人民日报',
#             patchtime=datetime.now(),
#             creator=creator
#         )
#         log.error('人民日报[http://www.people.com.cn/]数据更新失败，{}'.format(e))
#         return False
