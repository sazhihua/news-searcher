function getMoreTypeInfo() {
    $.ajax({
        url: '/api/getAllArticleType/',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            var articleType = data.data;
            var typeInfoHtmlStr = '';
            articleType.forEach(function (curType) {
                var curHref = curType.href;
                var curName = curType.name;
                typeInfoHtmlStr += "<li class='nav-item'><a class='nav-link nav-all-article-type' href='" + curHref + "'</a>" + curName + "</li>";
            })
            // document.getElementById("alertMoreTypeInfoContent").innerHTML = typeInfoHtmlStr;
            $('#alertMoreTypeInfoContent').html(typeInfoHtmlStr);
        },
        error: function () {
            utils.error("获取数据失败，请稍后再试")
        },
    })
}

function showLatestCloudPic() {
    console.log('dom 加载完成');
    var pageType = window.location.pathname.replaceAll('/', '');
    $.ajax({
        url: pageType === '' ? '/api/getLatestCloudPic/' : '/api/getLatestCloudPicByCode/',
        type: 'POST',
        data: pageType === '' ? null :{'pageType': pageType},
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                console.log("云图获取成功")
                var cloudPicData = data.data;
                var cloudPicResultId = cloudPicData.id;
                var cloudPicResultList = cloudPicData.list;
                var cloudContentHtmlStr = "";
                cloudPicResultList.forEach(function (curCloudPicResult) {
                    cloudContentHtmlStr += "<a class='btn btn-outline-secondary latest-cloud-content' href='/s?wd=" + curCloudPicResult + "'>" + curCloudPicResult + "</a>"
                })
                // document.getElementById("cloudPicArea").innerHTML = "<img class='rounded latest-cloud-pic' src='/static/img/cloudpic/" + cloudPicResultId + ".png'></img>";
                // document.getElementById("cloudContentArea").className = "recommend-hot-content";
                // document.getElementById("cloudContentArea").innerHTML = cloudContentHtmlStr;
                $('#cloudPicArea').html("<img class='rounded latest-cloud-pic' alt='cloudPicArea' src='/static/img/cloudpic/" + cloudPicResultId + ".png'></img>");
                $('#cloudContentArea').removeClass("text-center").html(cloudContentHtmlStr);
            } else {
                utils.error("获取数据失败，请稍后再试")
            }
        },
        error: function () {
            utils.error("获取数据失败，请稍后再试")
        }
    })
}