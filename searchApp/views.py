import traceback

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from searchApp.core.controller import htmlController, crawlersController, adminController
from searchApp.core.utils import funcUtils


# Create your views here.
def index(request):
    """
    首页--如果没有查询到参数则返回首页，否则返回的是查询结果页面
    :param request:
    :return:
    """
    if len(request.GET) == 0 or request.GET.get('wd') is None or request.GET.get('wd') == '':
        retHtml = 'index.html'
        types = htmlController.getArticleType()
        data = htmlController.getLatestNews()
        return render(request, retHtml, {
            'types': types,
            'data': data
        })
    else:
        retHtml = 'result.html'
        searchContent = request.GET.get('wd').strip()
        searchTime = request.GET.get('time') \
            if request.GET.get('time') == 'all' or request.GET.get('time') == 'day' or \
               request.GET.get('time') == 'week' or request.GET.get('time') == 'month' \
            else 'all'
        searchPage = funcUtils.pageParamToInt(request.GET.get('pn')) if request.GET.get('pn') is not None else 1
        searchMap = {'searchContent': searchContent,
                     'searchTime': searchTime,
                     'searchPage': searchPage
                     }
        data = htmlController.getData(searchMap)
        htmlController.addSearchLog(request)
        return render(request, retHtml, {
            'data': data
        })


def getIndexByType(request, *args, **kwargs):
    """
    根据类型获取首页
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    indexCode = str(kwargs['indextype'])
    indexType = htmlController.getIndexByType(indexCode)
    if not indexType:
        return render(request, 'msg.html', {
            'errcode': '404'
        })
    if len(request.GET) == 0 or request.GET.get('wd') is None or request.GET.get('wd') == '':
        retHtml = 'index.html'
        types = htmlController.getArticleType()
        data = htmlController.getLatestNewsByCode(indexCode)
        return render(request, retHtml, {
            'types': types,
            'data': data,
            'indexType': indexType,
        })
    else:
        retHtml = 'result.html'
        searchContent = request.GET.get('wd').strip()
        searchTime = request.GET.get('time') \
            if request.GET.get('time') == 'all' or request.GET.get('time') == 'day' or \
               request.GET.get('time') == 'week' or request.GET.get('time') == 'month' \
            else 'all'
        searchPage = funcUtils.pageParamToInt(request.GET.get('pn')) if request.GET.get('pn') is not None else 1
        searchMap = {'searchContent': searchContent,
                     'searchTime': searchTime,
                     'searchPage': searchPage
                     }
        data = htmlController.getData(searchMap)
        htmlController.addSearchLog(request)
        return render(request, retHtml, {
            'data': data,
            'indexType': indexType,
        })


def article(request, *args, **kwargs):
    """
    根据uuid获取文章
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    articleId = str(kwargs['articleId'])
    if not funcUtils.check_uuid4(articleId):
        return render(request, 'msg.html', {
            'errcode': '404'
        })
    data = htmlController.getNewsById(articleId)
    if not data:
        return render(request, 'msg.html', {
            'errcode': '404'
        })
    return render(request, 'article.html', {
        'data': data
    })


def helpOfArticleType(request):
    """
    文章类型帮助
    :param request:
    :return:
    """
    data = adminController.helpOfArticleType()
    return render(request, 'help.html', {
        'name': '类型',
        'data': data,
    })


def helpOfSourceSite(request):
    """
    文章来源帮助
    :param request:
    :return:
    """
    data = adminController.helpOfSourceSite()
    return render(request, 'help.html', {
        'name': '来源',
        'data': data
    })


def sysUpdate(request, *args, **kwargs):
    """
    系统升级（只有登录的管理员才能查看）
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    data = adminController.getLastUpdateInfo()
    return render(request, 'update.html', {
        'data': data
    })


def sysVersion(request):
    """
    系统版本
    :param request:
    :return:
    """
    return render(request, 'version.html')


def bigScreen(request):
    """
    大屏
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return render(request, 'bigscreen.html')
    else:
        return render(request, 'msg.html', {
            'errcode': '500'
        })


@csrf_exempt
@require_POST
def getBigScreenData(request):
    sourceEntities, typeEntities, ipEntities, pageviewEntities, searchEntities, updateEntities = adminController.getBigScreenData()
    return JsonResponse(data={'data': True, 'sourceEntities': sourceEntities, 'typeEntities': typeEntities,
                              'ipEntities': ipEntities, 'pageviewEntities': pageviewEntities,
                              'searchEntities': searchEntities, 'updateEntities': updateEntities})


@csrf_exempt
@require_POST
def updateAll(request):
    if request.user.is_authenticated:
        pageNum = request.POST.get('pageNum')
        updateType = str(request.POST.get('updateType'))
        result = crawlersController.updateAll(pageNum, request.user.username, updateType)
        return JsonResponse(data={'data': result})
    else:
        return render(request, 'msg.html', {
            'errcode': '500'
        })


@csrf_exempt
@require_POST
def updateSina(request):
    if request.user.is_authenticated:
        pageNum = request.POST.get('pageNum')
        result = crawlersController.updateSina(pageNum, request.user.username)
        return JsonResponse(data={'data': result})
    else:
        return render(request, 'msg.html', {
            'errcode': '500'
        })


@csrf_exempt
@require_POST
def updateNetease(request):
    if request.user.is_authenticated:
        pageNum = request.POST.get('pageNum')
        result = crawlersController.updateNetease(pageNum, request.user.username)
        return JsonResponse(data={'data': result})
    else:
        return render(request, 'msg.html', {
            'errcode': '500'
        })


@csrf_exempt
@require_POST
def updateSohu(request):
    if request.user.is_authenticated:
        pageNum = request.POST.get('pageNum')
        result = crawlersController.updateSohu(pageNum, request.user.username)
        return JsonResponse(data={'data': result})
    else:
        return render(request, 'msg.html', {
            'errcode': '500'
        })


@csrf_exempt
@require_POST
def updateCCTV(request):
    if request.user.is_authenticated:
        pageNum = request.POST.get('pageNum')
        result = crawlersController.updateCCTV(pageNum, request.user.username)
        return JsonResponse(data={'data': result})
    else:
        return render(request, 'msg.html', {
            'errcode': '500'
        })


@csrf_exempt
@require_POST
def updatePaper(request):
    if request.user.is_authenticated:
        result = crawlersController.updatePaper(request.user.username)
        return JsonResponse(data={'data': result})
    else:
        return render(request, 'msg.html', {
            'errcode': '500'
        })


@csrf_exempt
@require_POST
def updateIndex(request):
    if request.user.is_authenticated:
        result = crawlersController.updateIndex(request.user.username)
        return JsonResponse(data={'data': result})
    else:
        return render(request, 'msg.html', {
            'errcode': '500'
        })


@csrf_exempt
@require_POST
def deleteOldDatas(request):
    if request.user.is_authenticated:
        result = crawlersController.deleteOldDatas(request.user.username)
        return JsonResponse(data={'data': result})
    else:
        return render(request, 'msg.html', {
            'errcode': '500'
        })


@csrf_exempt
@require_POST
def testBackMethod(request):
    return JsonResponse(data={'data': True})


@csrf_exempt
@require_POST
def getAllArticleType(request):
    articleType = htmlController.getAllArticleType()
    return JsonResponse(data={'data': articleType})


@csrf_exempt
@require_POST
def getLatestCloudPic(request):
    createResult = htmlController.getLatestCloudPic()
    return JsonResponse(data={'data': createResult})


@csrf_exempt
@require_POST
def getLatestCloudPicByCode(request):
    pageType = request.POST.get('pageType')
    createResult = htmlController.getLatestCloudPicByCode(pageType)
    return JsonResponse(data={'data': createResult})


@csrf_exempt
@require_POST
def deleteAllCloudPics(request):
    if request.user.is_authenticated:
        htmlController.deleteAllCloudPics(request.user.username)
        return JsonResponse(data={'data': True})
    else:
        return render(request, 'msg.html', {
            'errcode': '500'
        })


@csrf_exempt
@require_POST
def getAutoCompleteValue(request):
    prefixValue = request.POST.get('prefixValue')
    autoCompleteValue = htmlController.getAutoCompleteValue(prefixValue)
    return JsonResponse(data={'data': autoCompleteValue})


@csrf_exempt
@require_POST
def reportCurNews(request):
    curId = request.POST.get('curId')
    reportResult = htmlController.reportCurNews(curId)
    return JsonResponse(data={'data': reportResult})


@csrf_exempt
@require_POST
def getRecommendData(request):
    searchContent = request.POST.get('searchContent').strip()
    data = htmlController.getRecommendData(searchContent)
    return JsonResponse(data=data)


@csrf_exempt
@require_POST
def getRecommendDataByArticle(request):
    curId = request.POST.get('id')
    data = htmlController.getRecommendDataByArticle(curId)
    return JsonResponse(data=data)


# 定时任务
scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
scheduler.add_jobstore(DjangoJobStore(), 'default')


@csrf_exempt
@require_POST
def regularUpdateStart(request):
    try:
        if request.user.is_authenticated:
            if scheduler.get_job('regularUpdate') is not None:
                raise ValueError('Job identifier (regularUpdate) conflicts with an existing job')
            else:
                scheduler.add_job(crawlersController.regularUpdate, 'interval', hours=4, id='regularUpdate',
                                  args=[request.user.username])
                scheduler.start()
            return JsonResponse(data={'data': True})
        else:
            return JsonResponse(data={'data': False})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse(data={'data': False, 'msg': str(e)})


@csrf_exempt
@require_POST
def regularUpdateClose(request):
    try:
        if request.user.is_authenticated:
            if scheduler.get_job('regularUpdate') is not None:
                scheduler.remove_job('regularUpdate')
                scheduler.shutdown()
            else:
                raise ValueError('Scheduler is not running')
            return JsonResponse(data={'data': True})
        else:
            return JsonResponse(data={'data': False})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse(data={'data': False, 'msg': str(e)})
