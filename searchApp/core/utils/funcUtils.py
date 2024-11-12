import uuid

import user_agents

from django.db import connection
from searchApp.config import logger

log = logger.createLogger("funcUtils")


def getSourceByName(name):
    """
    根据来源的名称获取来源id
    :param name: 来源名称，如新浪网
    :return: 来源id
    """
    with connection.cursor() as cursor:
        sql = 'select id from sourcesite where name = %s '
        cursor.execute(sql, name)
        log.info("执行sql：{}，参数：{}".format(sql, name))
        result = cursor.fetchall()
    if len(result) == 1:
        return result[0][0]
    else:
        return


def getTypeByName(name):
    """
    根据类型名称获取类型id
    :param name: 类型名称，如体育
    :return: 类型id
    """
    with connection.cursor() as cursor:
        sql = 'select id from articletype where name = %s '
        cursor.execute(sql, name)
        log.info("执行sql：{}，参数：{}".format(sql, name))
        result = cursor.fetchall()
    if len(result) == 1:
        return result[0][0]
    else:
        return


def ifArticleNotExist(url):
    """
    根据单据url判断单据是否已经存在
    :param url
    :return: True：添加新闻，False：取消添加
    """
    with connection.cursor() as cursor:
        sql = 'select 1 from article where url = %s '
        cursor.execute(sql, url)
        log.info("执行sql：{}，参数：{}".format(sql, url))
        result = cursor.fetchall()
    if len(result) == 0:
        return True
    return False


def check_uuid4(test_uuid, version=4):
    """
    判断参数是不是一个合格的uuid4格式
    :param test_uuid:
    :param version:
    :return:
    """
    try:
        return uuid.UUID(test_uuid).version == version
    except ValueError:
        return False


def pageParamToInt(string):
    """
    将收到的页码参数转为int
    :param string:
    :return:
    """
    try:
        return int(float(string)) if int(float(string)) > 0 else 1
    except ValueError:
        return 1


def objToStr(obj):
    """
    将参数转换为str
    :param obj:
    :return:
    """
    try:
        return str(obj) if obj is not None else ''
    except ValueError:
        return ''


def objIsNumber(obj):
    """
    判断参数是不是数字类型
    :param obj:
    :return:
    """
    try:
        float(obj)
        return True
    except ValueError:
        return False


def charIsLetter(char):
    """
    判断参数是不是英文字母
    :param char:
    :return:
    """
    if ('a' <= char <= 'z') or ('A' <= char <= 'Z'):
        return True
    else:
        return False


def getBrowserType(agent):
    """
    判断浏览器标识
    :param agent:
    :return:
    """
    temp = user_agents.parse(agent)
    return temp.browser.family, '1' if temp.is_mobile else '0'


def getNewsTitleById(curId):
    """
   根据id找新闻标题
   :param curId:
   :return:
   """
    with connection.cursor() as cursor:
        sql = 'select title from article where id = %s '
        cursor.execute(sql, curId)
        result = cursor.fetchall()
    return result[0][0]
