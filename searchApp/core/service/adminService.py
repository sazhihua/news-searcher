import json

from django.db import connection

from searchApp.config import logger

# create logger
log = logger.createLogger("adminService")


def helpOfArticleType():
    """
    文章类型帮助
    :return:
    """
    with connection.cursor() as cursor:
        sql = 'select id, name from articletype '
        cursor.execute(sql)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]

    return result


def helpOfSourceSite():
    """
    文章来源帮助
    :return:
    """
    with connection.cursor() as cursor:
        sql = 'select id, name from sourcesite '
        cursor.execute(sql)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]

    return result


def getLastUpdateInfo():
    """
    获取上次系统更新的信息
    :return:
    """
    with connection.cursor() as cursor:
        sql = 'select id, patchtime, info from patchlog order by patchtime desc limit 1 '
        cursor.execute(sql)
        description = cursor.description
        result = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
    if len(result) != 1:
        return
    return result[0]


def choicesOfArticleType():
    """
    管理员界面--类型下拉框
    :return:
    """
    with connection.cursor() as cursor:
        sql = 'select id, name from articletype '
        cursor.execute(sql)
        result = cursor.fetchall()
    return result


def choicesOfSourceSite():
    """
    管理员界面--来源下拉框
    :return:
    """
    with connection.cursor() as cursor:
        sql = 'select id, name from sourcesite '
        cursor.execute(sql)
        result = cursor.fetchall()
    return result


def getBigScreenData():
    """
    大屏数据
    :return:
    """

    # region 网站统计
    with connection.cursor() as cursor:
        sql = "select sourcesite.name as name, count(1) as value from article left join sourcesite " \
              "on sourcesite.id = article.source group by sourcesite.name "
        cursor.execute(sql)
        description = cursor.description
        sourceEntities = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
    # endregion
    # region 类型统计
    with connection.cursor() as cursor:
        sql = "select articletype.name as name, count(1) as value from article left join articletype " \
              "on articletype.id = article.type group by articletype.name "
        cursor.execute(sql)
        description = cursor.description
        typeEntities = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
    # endregion
    # region 地图统计
    with connection.cursor() as cursor:
        sql = "select ipaddress as name, count(1) as value, " \
              "sum(case when mobileflag = '0' then 1 else 0 end) as pc, " \
              "sum(case when mobileflag = '1' then 1 else 0 end) as mobile from searchlog group by ipaddress "
        cursor.execute(sql)
        description = cursor.description
        ipEntities = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
    # endregion
    # region 新闻访问统计
    with connection.cursor() as cursor:
        sql = "select title, pageview as value from article order by pageview desc limit 5 offset 0 "
        cursor.execute(sql)
        description = cursor.description
        pageviewEntities = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
    # endregion
    # region 最新搜索情况统计
    with connection.cursor() as cursor:
        sql = "select searchcontent, searchtime from searchlog order by searchtime desc limit 20 offset 0 "
        cursor.execute(sql)
        description = cursor.description
        searchEntities = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
    # endregion
    # region 最新更新情况统计
    with connection.cursor() as cursor:
        sql = "select info, patchtime from patchlog order by patchtime desc limit 20 offset 0 "
        cursor.execute(sql)
        description = cursor.description
        updateEntities = [dict(zip([col[0] for col in description], row)) for row in cursor.fetchall()]
    # endregion

    return sourceEntities, typeEntities, ipEntities, pageviewEntities, searchEntities, updateEntities
