from searchApp.core.service import adminService


def helpOfArticleType():
    """
    管理员界面--类型帮助
    :return:
    """
    return adminService.helpOfArticleType()


def helpOfSourceSite():
    """
    管理员界面--来源帮助
    :return:
    """
    return adminService.helpOfSourceSite()


def getLastUpdateInfo():
    """
    管理员界面--获取上次更新信息
    :return:
    """
    return adminService.getLastUpdateInfo()


def choicesOfArticleType():
    """
    管理员界面--类型下拉框
    :return:
    """
    return adminService.choicesOfArticleType()


def choicesOfSourceSite():
    """
    管理员界面--来源下拉框
    :return:
    """
    return adminService.choicesOfSourceSite()


def getBigScreenData():
    """
    大屏界面
    :return:
    """
    return adminService.getBigScreenData()
