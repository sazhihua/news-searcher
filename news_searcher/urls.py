"""news_searcher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic.base import RedirectView

from searchApp.views import *

"""
url模式： 注意需要将admin里访问的网页放在admin之前
    /admin：后台管理系统
    /：主页面
    /s：主页面，有参数时为搜索详情页面
    /(indexType)：对应articletype表中的site字段，如sport -> /sport
    /article/(uuid)：对应具体文章
    /about：关于
"""

urlpatterns = [
    re_path(r'^favicon.ico$', RedirectView.as_view(url=r'/static/img/favicon.ico')),
    path('admin/help/articletype/', helpOfArticleType, name='helpOfArticleType'),
    path('admin/help/sourcesite/', helpOfSourceSite, name='helpOfSourceSite'),
    path('admin/sys/update/', sysUpdate, name='sysUpdate'),
    path('admin/sys/version/', sysVersion, name='sysVersion'),
    path('admin/sys/bigscreen/', bigScreen, name='bigScreen'),
    path('admin/api/testBackMethod/', testBackMethod, name='testBackMethod'),
    path('admin/api/updateAll/', updateAll, name='updateAll'),
    path('admin/api/updateSina/', updateSina, name='updateSina'),
    path('admin/api/updateNetease/', updateNetease, name='updateNetease'),
    path('admin/api/updateSohu/', updateSohu, name='updateSohu'),
    path('admin/api/updateCCTV/', updateCCTV, name='updateCCTV'),
    path('admin/api/updatePaper/', updatePaper, name='updatePaper'),
    path('admin/api/updateIndex/', updateIndex, name='updateIndex'),
    path('admin/api/deleteOldDatas/', deleteOldDatas, name='deleteOldDatas'),
    path('admin/api/deleteAllCloudPics/', deleteAllCloudPics, name='deleteAllCloudPics'),
    path('admin/api/regularUpdateStart/', regularUpdateStart, name='regularUpdateStart'),
    path('admin/api/regularUpdateClose/', regularUpdateClose, name='regularUpdateClose'),
    path('admin/api/getBigScreenData/', getBigScreenData, name='getBigScreenData'),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('s', index, name='index-suffix'),
    path('<str:indextype>/', getIndexByType, name='index-type'),
    path('article/<str:articleId>/', article, name='article'),
    path('api/getAllArticleType/', getAllArticleType, name='getAllArticleType'),
    path('api/getLatestCloudPic/', getLatestCloudPic, name='getLatestCloudPic'),
    path('api/getLatestCloudPicByCode/', getLatestCloudPicByCode, name='getLatestCloudPicByCode'),
    path('api/getAutoCompleteValue/', getAutoCompleteValue, name='getAutoCompleteValue'),
    path('api/reportCurNews/', reportCurNews, name='reportCurNews'),
    path('api/getRecommendData/', getRecommendData, name='getRecommendData'),
    path('api/getRecommendDataByArticle/', getRecommendDataByArticle, name='getRecommendDataByArticle'),
]
