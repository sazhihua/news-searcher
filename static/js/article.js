function plusFontSize() {
    var cur = $('#main-content');
    var curFontSize = cur.attr('class');
    switch (curFontSize) {
        case 'fs-6':
            cur.removeClass('fs-6').addClass('fs-5');
            break;
        case 'fs-5':
            cur.removeClass('fs-5').addClass('fs-4');
            break;
        default:
    }
}

function dashFontSize() {
    var cur = $('#main-content');
    var curFontSize = cur.attr('class');
    switch (curFontSize) {
        case 'fs-4':
            cur.removeClass('fs-4').addClass('fs-5');
            break;
        case 'fs-5':
            cur.removeClass('fs-5').addClass('fs-6');
            break;
        default:
    }
}

function reportCurNews(curId) {
    utils.warn('正在提交单据...')
    setTimeout(function () {
        $.ajax({
            url: '/api/reportCurNews/',
            type: 'POST',
            data: {'curId': curId},
            dataType: 'json',
            success: function (data) {
                if (data.data) {
                    utils.success('工单已提交，我们会很快处理')
                } else {
                    utils.error("获取数据失败，请稍后再试")
                }
            },
            error: function () {
                utils.error("获取数据失败，请稍后再试")
            },
        })
    }, 2000);
}

function getRecommendDataByArticle() {
    let curId = $('#article-id').text();
    $.ajax({
        url: '/api/getRecommendDataByArticle/',
        type: 'POST',
        data: {'id': curId},
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                let recommend = `
                    <div class="row">
                        <span>相关推荐</span>
                    </div>`
                for (let res in data.result) {
                    recommend += `
                        <div class="row" style="margin-top: 10px;">
                        <div class="col-auto" style="padding-right: 0;">
                            <span class="left-circle-pic"></span>
                        </div>
                        <div class="col-auto" style="padding-right: 0;">
                            <small style="color: var(--bs-gray);">${new Date(data.result[res].publishtime).format('yyyy年MM月dd日 hh:mm')}</small>
                        </div>`
                    if (data.result[res].istoday == '1') {
                        recommend += `<div class="col-auto" style="padding: 0;"><span class="left-text-new">新</span></div>`
                    }
                    recommend += `
                        <div class="col-auto">
                            <a class="recommend-title" href="/article/${data.result[res].id}/" title="${data.result[res].title}">${data.result[res].title}</a>
                        </div>
                    </div>`
                }
                $('.main-recommend-div').css("padding", "20px 0").html(recommend);
            }
        },
        error: function () {
            console.log('获取推荐资讯失败，不展示相关区域');
        },
    })
}