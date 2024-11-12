from django.contrib import admin, messages
from django.http import JsonResponse
from django.utils.safestring import mark_safe

from searchApp import models

# Register your models here.
admin.site.site_header = 'News Searcher'
admin.site.site_title = 'News Searcher'
admin.site.index_title = 'News Searcher'


class Article(admin.ModelAdmin):
    list_display = ('id', 'type__name', 'source__name', 'title', 'publishtime', 'state_isenabled__name',)
    search_fields = ('id', 'title',)
    list_filter = ('publishtime', 'type', 'source', 'state_isenabled',)
    list_per_page = 20
    ordering = ('-timestamp_createdon',)

    actions = ['status_enable', 'status_disable', 'fc_view_type', 'fc_view_source']

    @admin.display(description='类型')
    def type__name(self, obj):
        result = models.ArticleType.objects.values('name').filter(id=obj.type)
        return result.get()['name'] if len(result) == 1 else obj.type

    @admin.display(description='来源')
    def source__name(self, obj):
        result = models.SourceSite.objects.values('name').filter(id=obj.source)
        return result.get()['name'] if len(result) == 1 else obj.source

    @admin.display(description='是否可用')
    def state_isenabled__name(self, obj):
        return '是' if str(obj.state_isenabled) == '1' else '否'

    def status_enable(self, request, queryset):
        for data in queryset:
            models.Article.objects.filter(id=data.id).update(state_isenabled='1')
        messages.add_message(request, messages.SUCCESS, '状态修改成功')

    def status_disable(self, request, queryset):
        for data in queryset:
            models.Article.objects.filter(id=data.id).update(state_isenabled='0')
        messages.add_message(request, messages.SUCCESS, '状态修改成功')

    def fc_view_type(self):
        pass

    def fc_view_source(self):
        pass

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False

    fc_view_type.short_description = ' 类型帮助'
    fc_view_type.icon = 'fa fa-bars'
    fc_view_type.type = ''  # https://element.eleme.cn/#/zh-CN/component/button
    fc_view_type.action_type = 1
    fc_view_type.action_url = '/admin/help/articletype/'

    fc_view_source.short_description = ' 来源帮助'
    fc_view_source.icon = 'fa fa-paperclip'
    fc_view_source.type = ''
    fc_view_source.action_type = 1
    fc_view_source.action_url = '/admin/help/sourcesite/'

    status_enable.short_description = ' 启用'
    status_enable.icon = 'fa fa-circle-check'
    status_enable.type = 'success'
    status_enable.confirm = '确定修改选定新闻的可用状态为可用？'

    status_disable.short_description = ' 禁用'
    status_disable.icon = 'fa fa-circle-xmark'
    status_disable.type = 'warning'
    status_disable.confirm = '确定修改选定新闻的可用状态为不可用？'


class ArticleType(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon', 'sortorder', 'showindex__name', 'custom__count', 'state_isenabled__name',)
    search_fields = ('name',)
    list_filter = ('showindex', 'state_isenabled',)
    list_per_page = 20
    ordering = ('sortorder',)

    actions = ['my_delete', 'status_enable', 'status_disable']

    @admin.display(description='计数')
    def custom__count(self, obj):
        return models.Article.objects.filter(type=obj.id).count()

    @admin.display(description='主页显示')
    def showindex__name(self, obj):
        return '是' if str(obj.showindex) == '1' else '否'

    @admin.display(description='是否可用')
    def state_isenabled__name(self, obj):
        return '是' if str(obj.state_isenabled) == '1' else '否'

    def status_enable(self, request, queryset):
        for data in queryset:
            models.ArticleType.objects.filter(id=data.id).update(state_isenabled='1')
        messages.add_message(request, messages.SUCCESS, '状态修改成功')

    def status_disable(self, request, queryset):
        for data in queryset:
            models.ArticleType.objects.filter(id=data.id).update(state_isenabled='0')
        messages.add_message(request, messages.SUCCESS, '状态修改成功')

    def has_delete_permission(self, request, obj=None):
        return False

    def my_delete(self, request, queryset):
        if len(queryset) != 1:
            return messages.add_message(request, messages.ERROR, '该操作不支持批量，请选择单条数据！')
        else:
            if str(queryset[0].sysinit) == '1':
                return messages.add_message(request, messages.ERROR, '系统预置的数据不可删除！')
            else:
                if len(models.Article.objects.filter(type=queryset[0].id)) > 0:
                    return messages.add_message(request, messages.ERROR, '该类型已被使用，不可删除！')
                models.ArticleType.objects.get(id=queryset[0].id).delete()
                return messages.add_message(request, messages.SUCCESS, '删除成功！')

    status_enable.short_description = ' 启用'
    status_enable.icon = 'fa fa-circle-check'
    status_enable.type = 'success'
    status_enable.confirm = '确定修改选定类型的可用状态为可用？'

    status_disable.short_description = ' 禁用'
    status_disable.icon = 'fa fa-circle-xmark'
    status_disable.type = 'warning'
    status_disable.confirm = '确定修改选定类型的可用状态为不可用？'

    my_delete.short_description = ' 删除'
    my_delete.icon = 'fa fa-trash-can'
    my_delete.type = 'danger'
    my_delete.confirm = '确定删除选中的数据吗？'


class SourceSite(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon__img', 'url', 'custom__count', 'sysinit__name', 'state_isenabled__name',)
    search_fields = ('name',)
    list_filter = ('state_isenabled',)
    list_per_page = 20
    ordering = ('id',)

    actions = ['my_delete', 'status_enable', 'status_disable']

    @admin.display(description='图标')
    def icon__img(self, obj):
        return mark_safe(f"<img src='" + obj.icon + "' alt='logo' style='width: 16px;'></img>")

    @admin.display(description='计数')
    def custom__count(self, obj):
        return models.Article.objects.filter(source=obj.id).count()

    @admin.display(description='系统预置')
    def sysinit__name(self, obj):
        return '是' if str(obj.sysinit) == '1' else '否'

    @admin.display(description='是否可用')
    def state_isenabled__name(self, obj):
        return '是' if str(obj.state_isenabled) == '1' else '否'

    def status_enable(self, request, queryset):
        for data in queryset:
            models.SourceSite.objects.filter(id=data.id).update(state_isenabled='1')
        messages.add_message(request, messages.SUCCESS, '状态修改成功')

    def status_disable(self, request, queryset):
        for data in queryset:
            models.SourceSite.objects.filter(id=data.id).update(state_isenabled='0')
        messages.add_message(request, messages.SUCCESS, '状态修改成功')

    def has_delete_permission(self, request, obj=None):
        return False

    def my_delete(self, request, queryset):
        if len(queryset) != 1:
            return messages.add_message(request, messages.ERROR, '该操作不支持批量，请选择单条数据！')
        else:
            if str(queryset[0].sysinit) == '1':
                return messages.add_message(request, messages.ERROR, '系统预置的数据不可删除！')
            else:
                if len(models.Article.objects.filter(source=queryset[0].id)) > 0:
                    return messages.add_message(request, messages.ERROR, '该来源已被使用，不可删除！')
                models.SourceSite.objects.get(id=queryset[0].id).delete()
                return messages.add_message(request, messages.SUCCESS, '删除成功！')

    status_enable.short_description = ' 启用'
    status_enable.icon = 'fa fa-circle-check'
    status_enable.type = 'success'
    status_enable.confirm = '确定修改选定来源的可用状态为可用？'

    status_disable.short_description = ' 禁用'
    status_disable.icon = 'fa fa-circle-xmark'
    status_disable.type = 'warning'
    status_disable.confirm = '确定修改选定来源的可用状态为不可用？'

    my_delete.short_description = ' 删除'
    my_delete.icon = 'fa fa-trash-can'
    my_delete.type = 'danger'
    my_delete.confirm = '确定删除选中的数据吗？'


class DocumentProcess(admin.ModelAdmin):
    list_display = ('id', 'type', 'relatedid', 'info', 'status__name', 'reviewer', 'createtime',)
    search_fields = ('type', 'reviewer',)
    list_filter = ('type', 'status', 'reviewer',)
    list_per_page = 20
    ordering = ('-createtime',)

    actions = ['process_pass', 'process_return']

    @admin.display(description='状态')
    def status__name(self, obj):
        status_dict = {'1': '制单', '2': '完成', '3': '退回'}
        return status_dict.get(str(obj.status)) if status_dict.get(str(obj.status)) is not None else '未知'

    def has_add_permission(self, request, obj=None):
        return False

    def process_pass(self, request, queryset):
        """
        审批通过流程：修改所对应的新闻id状态为不可用，修改工单的状态为2
        :param request:
        :param queryset:
        :return:
        """
        if len(queryset) != 1:
            return messages.add_message(request, messages.ERROR, '该操作不支持批量，请选择单条数据！')
        else:
            if str(queryset[0].status) != '1' and str(queryset[0].status) != '3':
                return messages.add_message(request, messages.ERROR, '只有制单或退回状态的单据可以进行该操作！')
            result = models.Article.objects.filter(id=queryset[0].relatedid)
            if len(result) == 0:
                return messages.add_message(request, messages.ERROR, '没有找到该条数据，新闻不存在！')
            else:
                result.update(state_isenabled='0')
                models.DocumentProcess.objects.filter(id=queryset[0].id).update(status='2',
                                                                                reviewer=request.user.username)
                return messages.add_message(request, messages.SUCCESS, '审批成功！')

    def process_return(self, request, queryset):
        """
        审批退回流程：修改工单的状态为3
        :param request:
        :param queryset:
        :return:
        """
        if len(queryset) != 1:
            return messages.add_message(request, messages.ERROR, '该操作不支持批量，请选择单条数据！')
        else:
            if str(queryset[0].status) != '1':
                return messages.add_message(request, messages.ERROR, '只有制单状态的单据可以进行该操作！')
            result = models.Article.objects.filter(id=queryset[0].relatedid)
            if len(result) == 0:
                return messages.add_message(request, messages.ERROR, '没有找到该条数据，新闻不存在！')
            else:
                models.DocumentProcess.objects.filter(id=queryset[0].id).update(status='3',
                                                                                reviewer=request.user.username)
                return messages.add_message(request, messages.SUCCESS, '审批成功！')

    process_pass.short_description = ' 审批通过'
    process_pass.icon = 'fa fa-circle-check'
    process_pass.type = 'success'
    process_pass.confirm = '确定审批通过该工单？'

    process_return.short_description = ' 审批退回'
    process_return.icon = 'fa fa-circle-xmark'
    process_return.type = 'warning'
    process_return.confirm = '确定审批退回该工单？'


class PatchLog(admin.ModelAdmin):
    list_display = ('id', 'type', 'info', 'creator', 'patchtime',)
    search_fields = ('type',)
    list_filter = ('type', 'creator',)
    list_per_page = 20
    ordering = ('-patchtime',)

    actions = []


class SearchLog(admin.ModelAdmin):
    list_display = ('id', 'searchcontent', 'searchtime', 'ip', 'ipaddress', 'browser', 'mobileflag')
    search_fields = ('searchcontent', 'ipaddress',)
    list_filter = ('browser', 'mobileflag',)
    list_per_page = 20
    ordering = ('-searchtime',)

    actions = []

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


admin.site.register(models.Article, Article)
admin.site.register(models.ArticleType, ArticleType)
admin.site.register(models.SourceSite, SourceSite)
admin.site.register(models.DocumentProcess, DocumentProcess)
admin.site.register(models.PatchLog, PatchLog)
admin.site.register(models.SearchLog, SearchLog)
