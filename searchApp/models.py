import uuid

from django.db import models
from django.utils import timezone

from searchApp.core.controller import adminController

state_isenabled_value = (('1', '是'), ('0', '否'))
status_value = (('1', '制单'), ('2', '完成'), ('3', '退回'))


# Create your models here.
class Article(models.Model):
    id = models.CharField(max_length=36, blank=False, primary_key=True, unique=True, default=uuid.uuid4())
    type = models.CharField(max_length=36, null=True, verbose_name='类型',
                            choices=adminController.choicesOfArticleType())
    source = models.CharField(max_length=36, null=True, verbose_name='来源',
                              choices=adminController.choicesOfSourceSite())
    tags = models.TextField(blank=True, null=True, verbose_name='标签')
    title = models.TextField(null=True, verbose_name='标题')
    content = models.TextField(null=True, verbose_name='内容')
    pic = models.CharField(max_length=256, blank=True, null=True, verbose_name='图片')
    url = models.CharField(max_length=256, blank=True, null=True, verbose_name='原文链接', db_index=True)
    publishtime = models.DateTimeField(null=True, verbose_name='发布时间', default=timezone.now)
    pageview = models.IntegerField(null=True, verbose_name='浏览量', default=0)
    state_isenabled = models.CharField(max_length=1, null=True, verbose_name='是否可用', choices=state_isenabled_value)
    timestamp_createdby = models.CharField(max_length=36, null=True, verbose_name='创建者')
    timestamp_createdon = models.DateTimeField(null=True, verbose_name='创建时间', default=timezone.now)
    timestamp_lastchangedby = models.CharField(max_length=36, null=True, verbose_name='修改者')
    timestamp_lastchangedon = models.DateTimeField(null=True, verbose_name='修改时间', default=timezone.now)
    txt01 = models.TextField(null=True, blank=True)
    txt02 = models.TextField(null=True, blank=True)
    var01 = models.CharField(max_length=1, null=True, blank=True, db_index=True)
    var02 = models.CharField(max_length=100, null=True, blank=True)
    num01 = models.IntegerField(null=True, blank=True)
    num02 = models.IntegerField(null=True, blank=True)
    time01 = models.DateTimeField(null=True, blank=True)
    time02 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'article'
        verbose_name = '新闻'
        verbose_name_plural = '新闻'


class ArticleType(models.Model):
    id = models.CharField(max_length=36, blank=False, primary_key=True, unique=True, default=uuid.uuid4())
    name = models.CharField(max_length=100, null=True, verbose_name='名称')
    code = models.CharField(max_length=36, null=True, verbose_name='编号')
    icon = models.CharField(max_length=256, blank=True, null=True, verbose_name='图标')
    sortorder = models.IntegerField(null=True, verbose_name='排序')
    showindex = models.CharField(max_length=1, null=True, verbose_name='主页显示', choices=state_isenabled_value)
    state_isenabled = models.CharField(max_length=1, null=True, verbose_name='是否可用', choices=state_isenabled_value)
    timestamp_createdby = models.CharField(max_length=36, null=True, verbose_name='创建者')
    timestamp_createdon = models.DateTimeField(null=True, verbose_name='创建时间', default=timezone.now)
    timestamp_lastchangedby = models.CharField(max_length=36, null=True, verbose_name='修改者')
    timestamp_lastchangedon = models.DateTimeField(null=True, verbose_name='修改时间', default=timezone.now)
    txt01 = models.TextField(null=True, blank=True)
    num01 = models.IntegerField(null=True, blank=True)
    time01 = models.DateTimeField(null=True, blank=True)
    sysinit = models.CharField(max_length=1, null=True, verbose_name='系统预置', choices=state_isenabled_value)

    class Meta:
        db_table = 'articletype'
        verbose_name = '新闻类型'
        verbose_name_plural = '新闻类型'


class SourceSite(models.Model):
    id = models.CharField(max_length=36, blank=False, primary_key=True, unique=True, default=uuid.uuid4())
    name = models.CharField(max_length=100, null=True, verbose_name='名称')
    icon = models.CharField(max_length=256, blank=True, null=True, verbose_name='图标')
    url = models.CharField(max_length=256, blank=True, null=True, verbose_name='地址')
    state_isenabled = models.CharField(max_length=1, null=True, verbose_name='是否可用', choices=state_isenabled_value)
    timestamp_createdby = models.CharField(max_length=36, null=True, verbose_name='创建者')
    timestamp_createdon = models.DateTimeField(null=True, verbose_name='创建时间', default=timezone.now)
    timestamp_lastchangedby = models.CharField(max_length=36, null=True, verbose_name='修改者')
    timestamp_lastchangedon = models.DateTimeField(null=True, verbose_name='修改时间', default=timezone.now)
    txt01 = models.TextField(null=True, blank=True)
    num01 = models.IntegerField(null=True, blank=True)
    time01 = models.DateTimeField(null=True, blank=True)
    sysinit = models.CharField(max_length=1, null=True, verbose_name='系统预置', choices=state_isenabled_value)

    class Meta:
        db_table = 'sourcesite'
        verbose_name = '新闻来源'
        verbose_name_plural = '新闻来源'


class PatchLog(models.Model):
    id = models.CharField(max_length=36, blank=False, primary_key=True, unique=True, default=uuid.uuid4())
    type = models.CharField(max_length=36, null=True, verbose_name='类型')
    info = models.TextField(null=True, verbose_name='信息')
    patchtime = models.DateTimeField(null=True, verbose_name='升级时间', default=timezone.now)
    creator = models.CharField(max_length=36, null=True, verbose_name='创建者')

    class Meta:
        db_table = 'patchlog'
        verbose_name = '升级日志'
        verbose_name_plural = '升级日志'


class SearchLog(models.Model):
    id = models.CharField(max_length=36, blank=False, primary_key=True, unique=True, default=uuid.uuid4())
    searchcontent = models.TextField(null=True, verbose_name='搜索内容')
    searchtime = models.DateTimeField(null=True, verbose_name='搜索时间')
    ip = models.CharField(max_length=30, null=True, verbose_name='操作IP')
    ipaddress = models.TextField(null=True, verbose_name='IP归属地')
    browser = models.TextField(null=True, verbose_name='浏览器标识')
    mobileflag = models.CharField(max_length=1, null=True, verbose_name='移动端标识', choices=state_isenabled_value)

    class Meta:
        db_table = 'searchlog'
        verbose_name = '搜索日志'
        verbose_name_plural = '搜索日志'


class DocumentProcess(models.Model):
    id = models.CharField(max_length=36, blank=False, primary_key=True, unique=True, default=uuid.uuid4())
    type = models.CharField(max_length=36, null=True, verbose_name='类型')
    relatedid = models.CharField(max_length=36, null=True, verbose_name='关联ID')
    info = models.TextField(null=True, verbose_name='信息')
    status = models.CharField(max_length=1, null=True, verbose_name='审阅状态', choices=status_value)
    createtime = models.DateTimeField(null=True, verbose_name='创建时间', default=timezone.now)
    reviewer = models.CharField(max_length=36, null=True, verbose_name='审阅人')

    class Meta:
        db_table = 'documentprocess'
        verbose_name = '工单'
        verbose_name_plural = '工单'
