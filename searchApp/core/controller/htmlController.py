from searchApp.core.service import htmlService, searchService


def getArticleType():
    return htmlService.getArticleType()


def getAllArticleType():
    return htmlService.getAllArticleType()


def getIndexByType(site):
    return htmlService.getIndexByType(site)


def getLatestNews():
    return htmlService.getLatestNews()


def getLatestCloudPic():
    return htmlService.getLatestCloudPic()


def getLatestNewsByCode(indexCode):
    return htmlService.getLatestNewsByCode(indexCode)


def getLatestCloudPicByCode(indexCode):
    return htmlService.getLatestCloudPicByCode(indexCode)


def getNewsById(articleId):
    return htmlService.getNewsById(articleId)


def getAutoCompleteValue(prefixValue):
    return htmlService.getAutoCompleteValue(prefixValue)


def deleteAllCloudPics(username):
    return htmlService.deleteAllCloudPics(username)


def reportCurNews(curId):
    return htmlService.reportCurNews(curId)


def getData(searchMap):
    return searchService.getData(searchMap)


def addSearchLog(request):
    """
    管理员--增加搜索日志
    :param request:
    :return:
    """
    return htmlService.addSearchLog(request)


def getRecommendData(searchContent):
    return searchService.getRecommendData(searchContent)


def getRecommendDataByArticle(curId):
    return searchService.getRecommendDataByArticle(curId)
