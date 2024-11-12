import time
import traceback
import uuid
from datetime import datetime

from searchApp.config import logger
from searchApp.core.service import sinaNewsService, neteaseNewsService, sohuNewsService, cctvNewsService, \
    paperNewsService, indexService
from searchApp.models import PatchLog

log = logger.createLogger('crawlersController')


def updateAll(pageNum, userName, updateType):
    try:
        start = time.clock()
        neteaseNewsService.crawler(pageNum, userName)
        sinaNewsService.crawler(pageNum, userName)
        sohuNewsService.crawler(pageNum, userName)
        cctvNewsService.crawler(pageNum, userName)
        if updateType == '1':
            paperNewsService.crawler(userName)
        indexService.deleteOldDatas(userName)  # 删除旧数据（只保留90天新闻）
        indexService.updateIndex(userName)
        end = time.clock()
        log.info('数据更新完成，用时{}分'.format(round((end - start) / 60, 4)))
        PatchLog.objects.create(
            id=uuid.uuid4(),
            type='Update',
            info='数据更新完成，用时{}分'.format(round((end - start) / 60, 4)),
            patchtime=datetime.now(),
            creator=userName
        )
        return True
    except:
        traceback.print_exc()
        log.error('数据更新时出现异常，请联系管理员')
        PatchLog.objects.create(
            id=uuid.uuid4(),
            type='UpdateError',
            info='数据更新完失败，用时{}分，请查看具体更新错误信息'.format(round((end - start) / 60, 4)),
            patchtime=datetime.now(),
            creator=userName
        )
        return False


def updateSina(pageNum, userName):
    return sinaNewsService.crawler(pageNum, userName)


def updateNetease(pageNum, userName):
    return neteaseNewsService.crawler(pageNum, userName)


def updateSohu(pageNum, userName):
    return sohuNewsService.crawler(pageNum, userName)


def updateCCTV(pageNum, userName):
    return cctvNewsService.crawler(pageNum, userName)


def updatePaper(userName):
    return paperNewsService.crawler(userName)


def updateIndex(userName):
    return indexService.updateIndex(userName)


def deleteOldDatas(userName):
    return indexService.deleteOldDatas(userName)


def regularUpdate(userName):
    updateAll(2, userName, '2')
