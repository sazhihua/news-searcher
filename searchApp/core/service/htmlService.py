import uuid
from datetime import datetime

from django.db import connection
from searchApp.config import logger
from searchApp.core.utils import cloudPicUtils, funcUtils
from searchApp.models import PatchLog, DocumentProcess, SearchLog

log = logger.createLogger("htmlService")


def getArticleType():
    """
    获取新闻类型用于首页展示
    :return:
    """
    with connection.cursor() as cursor:
        sql = "select name, concat('/', code) as href from articletype where " \
              "showindex = '1' and state_isenabled = '1' order by sortorder "
        cursor.execute(sql)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]

    return result


def getAllArticleType():
    """
    获取全部新闻类型
    :return:
    """
    with connection.cursor() as cursor:
        sql = "select name, concat('/',code) as href from articletype where state_isenabled = '1' order by sortorder "
        cursor.execute(sql)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]

    return result


def getIndexByType(code):
    """
    根据url后缀判断新闻类型
    :param code:
    :return:
    """
    with connection.cursor() as cursor:
        sql = "select name from articletype where code = %s and state_isenabled = '1' "
        cursor.execute(sql, code)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
    if len(result) != 1:
        return False
    return result[0]['name']


def getLatestNews():
    """
    获取10条最新新闻，用于首页展示
    :return:
    """
    with connection.cursor() as cursor:
        sql = "select article.id, article.title, article.publishtime, article.pic, sourcesite.icon, sourcesite.name " \
              "from article left join sourcesite on article.source = sourcesite.id " \
              "where article.state_isenabled = '1' and sourcesite.state_isenabled = '1' " \
              "and var01 = '1' order by article.publishtime desc limit 10 offset 0 "
              # "order by article.publishtime desc limit 10 offset 0 "
              # "and var01 = '1' limit 10 offset 0 "
        cursor.execute(sql)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]

    return result


def getLatestCloudPic():
    """
    根据最新的500条新闻生成云图
    :return:
    """
    with connection.cursor() as cursor:
        sql = "select article.title, article.tags from article where state_isenabled = '1'" \
              "order by article.publishtime desc limit 500 offset 0 "
        cursor.execute(sql)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
    createResult = cloudPicUtils.buildCloudPic(result)

    return createResult


def getLatestNewsByCode(indexCode):
    """
    根据新闻类别获取最新的10条新闻置于相对应的主页
    :param indexCode: sports...
    :return:
    """
    with connection.cursor() as cursor:
        sql = "select article.id, article.title, article.publishtime, article.pic, sourcesite.icon, sourcesite.name " \
              "from article left join sourcesite on article.source = sourcesite.id where article.type = " \
              "(select id from articletype where code = %s ) and article.state_isenabled = '1' " \
              "and var01 = '1' order by article.publishtime desc limit 10 offset 0 "
              # "and sourcesite.state_isenabled = '1' order by article.publishtime desc limit 10 offset 0 "
        cursor.execute(sql, indexCode)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]

    return result


def getLatestCloudPicByCode(indexCode):
    """
    根据最新的相对应的新闻类别的500条新闻生成云图
    :return:
    """
    with connection.cursor() as cursor:
        sql = "select article.title, article.tags from article where article.type = " \
              "(select id from articletype where code = %s ) and state_isenabled = '1'" \
              "order by article.publishtime desc limit 500 offset 0 "
        cursor.execute(sql, indexCode)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
    createResult = cloudPicUtils.buildCloudPic(result)

    return createResult


def getNewsById(articleId):
    """
    根据id获取新闻
    :param articleId:
    :return:
    """
    with connection.cursor() as cursor:
        sql = "select article.id, articletype.name as typename, sourcesite.name as sourcename, " \
              "sourcesite.icon as icon, article.tags, article.title, " \
              "article.content, article.pic, article.url, article.publishtime, article.pageview from article " \
              "left join articletype on article.type = articletype.id " \
              "left join sourcesite on article.source = sourcesite.id " \
              "where article.id = %s and article.state_isenabled = '1' and articletype.state_isenabled = '1' " \
              "and sourcesite.state_isenabled = '1' "
        params = (articleId,)
        cursor.execute(sql, params)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
    if len(result) != 1:
        return False
    with connection.cursor() as cursor:
        updateSql = "update article set pageview = pageview + 1 where id = %s "
        cursor.execute(updateSql, params)
    return result[0]


def getAutoCompleteValue(prefixValue):
    """
    获取自动补全
    :param prefixValue:
    :return:
    """
    with connection.cursor() as cursor:
        sql = "select term from index_article where term like %s limit 5 offset 0 "
        params = (prefixValue + '%',)
        cursor.execute(sql, params)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]

    return result


def deleteAllCloudPics(username):
    """
    删除服务器云图文件夹所有文件
    :param username:
    :return:
    """
    PatchLog.objects.create(
        id=uuid.uuid4(),
        type='Delete',
        info='删除已生成的云图文件夹中的所有内容',
        patchtime=datetime.now(),
        creator=username
    )
    log.warning('云图文件夹已被清空')
    return cloudPicUtils.deleteAllCloudPics()


def reportCurNews(curId):
    """
    举报新闻
    :param curId:
    :return:
    """
    DocumentProcess.objects.create(
        id=uuid.uuid4(),
        type='举报',
        relatedid=curId,
        info='举报新闻：' + curId,
        status='1',
        createtime=datetime.now(),
        reviewer=None,
    )
    log.info('举报信息已提交')
    return True


def addSearchLog(request):
    """
    管理员--增加搜索日志
    :param request:
    :return:
    """
    browser, mobileflag = funcUtils.getBrowserType(request.META.get('HTTP_USER_AGENT', 'unknown'))
    SearchLog.objects.create(
        id=uuid.uuid4(),
        searchcontent=request.GET.get('wd').strip(),
        searchtime=datetime.now(),
        ip=request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else request.META[
            'REMOTE_ADDR'],
        ipaddress='山东',
        browser=browser,
        mobileflag=mobileflag
    )
    return True
