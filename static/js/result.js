/**
 * 页面加载完成重置html标题并填充搜索框和查询参数
 */
// $().ready(function () {
//     var titleName = utils.getQuery('wd');
//     if (titleName !== '') {
//         $('title').html(titleName + '_News Searcher');
//         $('#searchInput').val(titleName);
//     } else {
//         $('title').html('搜索结果_News Searcher');
//     }
//     $('#searchType-1').val(['all', 'day', 'week', 'month'].includes(utils.getQuery('time')) ? utils.getQuery('time') : 'all');
//     // var typeList = [utils.getQuery('time')];
//     // var arrayList = [Array.from($('#searchType-1 option'), item => item.value)];
//     // for (var i = 0; i < typeList.length; i++) {
//     //     if (arrayList[i].includes(typeList[i])) {
//     //         $('#searchType-' + i).val(typeList[i]);
//     //     } else {
//     //         $('#searchType-' + i).val(arrayList[i][0]);
//     //     }
//     // }
// });

/**
 * 分页插件
 * 参数cur是当前页数
 * 参数all表示总页数
 * 参数count可选，默认为10，表示显示的最大页数范围
 */
(function ($) {
    $.fn.pagination = function (cur, all, count) {
        //容错处理
        if (all <= 0) {
            all = 1;
        }
        if (cur <= 0) {
            cur = 1;
        } else if (cur > all) {
            cur = all;
        }
        //默认显示页数为10
        if (!count) {
            count = 10;
        } else if (count < 1) {
            count = 1;
        }
        //计算显示的页数
        var from = cur - parseInt(count / 2);
        var to = cur + parseInt(count / 2) + (count % 2) - 1;
        //显示的页数容处理
        if (from <= 0) {
            from = 1;
            to = from + count - 1;
            if (to > all) {
                to = all;
            }
        }
        if (to > all) {
            to = all;
            from = to - count + 1;
            if (from <= 0) {
                from = 1;
            }
        }
        //写入（可以根据自己需求修改）
        if (cur > 1) {
            // var prev = $("<li><a href='javascript:;'>&laquo;</a></li>");
            var prev = $("<li class='page-item'><a class='page-link' href='" + utils.setQueryParam('pn', cur - 1) + "'>&laquo;上一页</a></li>");
            this.append(prev);
        }
        for (var i = from; i <= to; i++) {
            if (i == cur) {
                // var li = $("<li class='active'><a href='javascript:;'>" + i + "</a></li>");
                var li = $("<li class='page-item active'><a class='page-link' href='#'>" + i + "</a></li>");
                this.append(li);
            } else {
                // var li = $("<li><a href='javascript:;'>" + i + "</a></li>");
                var li = $("<li class='page-item'><a class='page-link' href='" + utils.setQueryParam('pn', i) + "'>" + i + "</a></li>");
                this.append(li);
            }
        }
        if (cur < all) {
            // var prev = $("<li><a href='javascript:;'>&raquo;</a></li>");
            var prev = $("<li class='page-item'><a class='page-link' href='" + utils.setQueryParam('pn', cur + 1) + "'>下一页&raquo;</a></li>");
            this.append(prev);
        }
    }
})(jQuery);

function getRecommendData() {
    let content = utils.getQuery('wd').replace(/[`:_.~!@#$%^&*() \+ =<>?"{}|, \/ ;' \\ [ \] ·~！@#￥%……&*（）—— \+ ={}|《》？：“”【】、；‘’，。、]/g, '');
    $.ajax({
        url: '/api/getRecommendData/',
        type: 'POST',
        data: {'searchContent': content},
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                let recommend = `
                    <div class="card mb-3 border-light" style="width: 90%;">
                        <div class="card-header" style="background-color: white; border-bottom: 0;">
                            <span>推荐阅读</span>
                            <i class="bi bi-chevron-down"></i></small>
                        </div>
                        <div class="card-body">`
                for (let res in data.result) {
                    recommend += `
                            <div class="row" style="margin-bottom: 4px;">
                                <div class="col-auto recommend-number">
                                    <span style="color: var(--bs-gray);">${Number(res) + 1}</span>
                                </div>
                                <div class="col">
                                    <a class='text-truncate-1 recommend-title' href='/article/${data.result[res].id}/' 
                                    title='${data.result[res].title}'>${data.result[res].title}</a>
                                </div>`
                    if (data.result[res].istoday == '1') {
                        recommend += `<div class="col-auto"><span class="recommend-info">新</span></div>`
                    }
                    recommend += `</div>`
                }
                recommend += `</div></div>`
                recommend = recommend.replace('var(--bs-gray)', 'var(--bs-red)');
                recommend = recommend.replace('var(--bs-gray)', 'var(--bs-orange)')
                recommend = recommend.replace('var(--bs-gray)', 'var(--bs-yellow)')
                $('#recommend').html(recommend);
            } else {
                console.log('无划分结果，不展示推荐内容')
            }
        },
        error: function () {
            console.log('无划分结果，不展示推荐内容')
        },
    })
}