// 用于搜索框联想
$(function () {
    $('#searchInput').autocomplete({
        source: function (request, response) {
            var params = request.term.trim();
            if (params == '' || params.length == 0) {
                return;
            }
            var optionsList = [];
            $.ajax({
                url: '/api/getAutoCompleteValue/',
                type: 'POST',
                data: {'prefixValue': params},
                dataType: 'json',
                success: function (data) {
                    $.each(data.data, function (key, value) {
                        optionsList.push(value.term)
                    })
                    response(optionsList);
                },
                error: function () {
                    utils.error("获取数据失败，请稍后再试")
                },
            })
        },
        select: function (event, ui) {
            window.location.href = '/s?' + 'wd=' + ui.item.value + '&type=title&time=all';
        }
    })
})

/**
 * 日期格式化
 * @param format
 * @returns {*}
 */
Date.prototype.format = function(format) {
    var o = {
        "M+": this.getMonth() + 1, //month
        "d+": this.getDate(), //day
        "h+": this.getHours(), //hour
        "m+": this.getMinutes(), //minute
        "s+": this.getSeconds(), //second
        "q+": Math.floor((this.getMonth() + 3) / 3), //quarter
        "S": this.getMilliseconds() //millisecond
    }
    if (/(y+)/.test(format)) format = format.replace(RegExp.$1,
        (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(format))
            format = format.replace(RegExp.$1,
                RegExp.$1.length == 1 ? o[k] :
                ("00" + o[k]).substr(("" + o[k]).length));
    return format;
}

var utils = {
    /**
     * 弹出消息框
     * @param msg 消息内容
     * @param type 消息框类型（参考bootstrap的alert）
     */
    message: function (msg, type) {
        var messageType = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']
        if (messageType.indexOf(type) === -1) {
            return;
        }
        // 创建bootstrap的alert元素
        var divElement = $("<div></div>").addClass('alert').addClass('alert-' + type).addClass('alert-dismissible').addClass('col-md-4').addClass('col-md-offset-4');
        divElement.css({ // 消息框的定位样式
            "position": "absolute",
            "top": "80px",
            "left": 0,
            "right": 0,
            "margin": "auto",
        });
        var circleType = '';
        switch (type) {
            case 'primary':
                circleType = '<i class="bi bi-dash-circle"></i>';
                break;
            case 'danger':
                circleType = '<i class="bi bi-x-circle"></i>';
                break;
            case 'warning':
                circleType = '<i class="bi bi-exclamation-circle"></i>';
                break;
            case 'info':
                circleType = '<i class="bi bi-info-circle"></i>';
                break;
            default:
                circleType = '<i class="bi bi-check-circle"></i>';
        }
        msg = msg || type;
        divElement.html(circleType + msg); // 设置消息框的内容
        // 消息框添加可以关闭按钮
        var closeBtn = $('<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>');
        $(divElement).append(closeBtn);
        // 消息框放入到页面中
        $('body').append(divElement);
        var isIn = false; // 鼠标是否在消息框中

        divElement.on({ // 在setTimeout执行之前先判定鼠标是否在消息框中
            mouseover: function () {
                isIn = true;
            },
            mouseout: function () {
                isIn = false;
            }
        });

        // 短暂延时后上浮消失
        setTimeout(function () {
            var IntervalMS = 20; // 每次上浮的间隔毫秒
            var floatSpace = 60; // 上浮的空间(px)
            var nowTop = divElement.offset().top; // 获取元素当前的top值
            var stopTop = nowTop - floatSpace;  // 上浮停止时的top值
            divElement.fadeOut(IntervalMS * floatSpace); // 设置元素淡出

            var upFloat = setInterval(function () { // 开始上浮
                if (nowTop >= stopTop) { // 判断当前消息框top是否还在可上升的范围内
                    divElement.css({"top": nowTop--}); // 消息框的top上升1px
                } else {
                    clearInterval(upFloat); // 关闭上浮
                    divElement.remove();  // 移除元素
                }
            }, IntervalMS);

            if (isIn) { // 如果鼠标在setTimeout之前已经放在的消息框中，则停止上浮
                clearInterval(upFloat);
                divElement.stop();
            }

            divElement.hover(function () { // 鼠标悬浮时停止上浮和淡出效果，过后恢复
                clearInterval(upFloat);
                divElement.stop();
            }, function () {
                divElement.fadeOut(IntervalMS * (nowTop - stopTop)); // 这里设置元素淡出的时间应该为：间隔毫秒*剩余可以上浮空间
                upFloat = setInterval(function () { // 继续上浮
                    if (nowTop >= stopTop) {
                        divElement.css({"top": nowTop--});
                    } else {
                        clearInterval(upFloat); // 关闭上浮
                        divElement.remove();  // 移除元素
                    }
                }, IntervalMS);
            });
        }, 1500);
    },

    /**
     * 蓝底提示框
     * @param msg 消息内容 dash-circle
     */
    alert: function (msg) {
        utils.message(msg, 'primary');
    },

    /**
     * 红底错误提示框
     * @param msg 消息内容 x-circle
     */
    error: function (msg) {
        utils.message(msg, 'danger');
    },

    /**
     * 黄底提示提示框
     * @param msg 消息内容 exclamation-circle
     */
    warn: function (msg) {
        utils.message(msg, 'warning');
    },

    /**
     * 绿色信息提示框
     * @param msg 消息内容 info-circle
     */
    info: function (msg) {
        utils.message(msg, 'info');
    },

    /**
     * 成功提示框
     * @param msg 消息内容 check-circle
     */
    success: function (msg) {
        utils.message(msg, 'success');
    },

    /**
     * 获取url参数
     * @param key
     * @returns {string}
     */
    getQuery: function (key) {
        var reg = new RegExp("(^|&)" + key + "=([^&]*)(&|$)", "i");
        var r;
        var search = decodeURIComponent(window.location.search); //中文编码问题
        if (search) {
            var r = search.substring(1).match(reg);
        }
        if (r != null) {
            return r[2];
        }
        // else if (window.location.hash) {
        //     r = window.location.hash.substr(3).match(reg);
        //     if (r != null) return unescape(r[2])
        // }
        return '';
    },

    /**
     * 更改url参数
     * @param arg 需要修改的参数
     * @param val 修改后的值
     * @returns {string|string}
     */
    setQueryParam: function (arg, val) {
        var search = window.location.search;
        var pattern = arg + '=([^&]*)';
        var replaceText = arg + '=' + val;
        return search.match(pattern) ? search.replace(eval('/(' + arg + '=)([^&]*)/gi'), replaceText) : (search.match('[\?]') ? search + '&' + replaceText : search + '?' + replaceText);
    },

    /**
     * 转义字符串
     * @param string
     * @returns {string}
     */
    escapeHTML: function (string) {
        string = '' + string;
        return string.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&apos;");
    },

    /**
     * 反转义字符串
     * @param string
     * @returns {string}
     */
    unescapeHTML: function (string) {
        string = '' + string;
        return string.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/&apos;/g, "'");
    },

    /**
     * 遮罩层加载中
     * @param title 标题
     */
    loading: function (title) {
        var html = [];
        title = title || "加载中...";
        if ($("#loading-index").length > 0) {
            $("#loading-mask").show();
            $("#loading-index .message").html(title);
            $("#loading-index").show();
        } else {
            html.push("<div class='loading-mask' id='loading-mask'></div>");
            html.push('<div class="loading-index" id="loading-index"><div class="loading-inner text-light"><div class="spinner-border spinner-border-sm" role="status"></div>' + title + '</div></div></div>')
            var $loading = $(html.join(""));
            $("body").append($loading);
            $loading.show();
        }
    },

    /**
     * 关闭加载中遮罩层
     */
    loaded: function () {
        $("#loading-mask").hide();
        $("#loading-index").hide();
    }
}
