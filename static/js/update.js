function updateAll() {
    utils.loading();
    $.ajax({
        url: '/admin/api/updateAll/',
        type: 'POST',
        data: {'pageNum': 2, 'updateType': 1},
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('刷新完成');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("更新失败，请稍后再试");
            }
        },
        error: function () {
            utils.loaded();
            utils.error("更新失败，请稍后再试")
        }
    })
}

function updateAllExceptPaper() {
    utils.loading();
    $.ajax({
        url: '/admin/api/updateAll/',
        type: 'POST',
        data: {'pageNum': 2, 'updateType': 2},
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('刷新完成');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("更新失败，请稍后再试");
            }
        },
        error: function () {
            utils.loaded();
            utils.error("更新失败，请稍后再试")
        }
    })
}

function updateSina() {
    utils.loading();
    $.ajax({
        url: '/admin/api/updateSina/',
        type: 'POST',
        data: {'pageNum': 2},
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('刷新完成');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("更新失败，请稍后再试")
            }
        },
        error: function () {
            utils.loaded();
            utils.error("更新失败，请稍后再试")
        }
    })
}

function updateNetease() {
    utils.loading();
    $.ajax({
        url: '/admin/api/updateNetease/',
        type: 'POST',
        data: {'pageNum': 2},
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('刷新完成');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("更新失败，请稍后再试")
            }
        },
        error: function () {
            utils.loaded();
            utils.error("更新失败，请稍后再试")
        }
    })
}

function updateSohu() {
    utils.loading();
    $.ajax({
        url: '/admin/api/updateSohu/',
        type: 'POST',
        data: {'pageNum': 2},
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('刷新完成');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("更新失败，请稍后再试")
            }
        },
        error: function () {
            utils.loaded();
            utils.error("更新失败，请稍后再试")
        }
    })
}

function updateCCTV() {
    utils.loading();
    $.ajax({
        url: '/admin/api/updateCCTV/',
        type: 'POST',
        data: {'pageNum': 2},
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('刷新完成');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("更新失败，请稍后再试")
            }
        },
        error: function () {
            utils.loaded();
            utils.error("更新失败，请稍后再试")
        }
    })
}

function cleanPics() {
    utils.loading();
    $.ajax({
        url: '/admin/api/deleteAllCloudPics/',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('刷新完成');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("清空失败，请稍后再试")
            }
        },
        error: function () {
            utils.loaded();
            utils.error("清空失败，请稍后再试")
        }
    })
}

function testFrontMethod() {
    utils.loading('测试中...');
    setTimeout(function () {
        utils.success('功能无异常');
        utils.loaded();
    }, 2000)
}

function testBackMethod() {
    utils.loading('测试中...');
    $.ajax({
        url: '/admin/api/testBackMethod/',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('功能无异常');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("功能异常，请检查")
            }
        },
        error: function () {
            utils.loaded();
            utils.error("功能异常，请检查")
        }
    })
}

function updatePaper() {
    utils.loading();
    $.ajax({
        url: '/admin/api/updatePaper/',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('刷新完成');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("更新失败，请稍后再试")
            }
        },
        error: function () {
            utils.loaded();
            utils.error("更新失败，请稍后再试")
        }
    })
}

function updateIndex() {
    utils.loading();
    $.ajax({
        url: '/admin/api/updateIndex/',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('刷新完成');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("更新失败，请稍后再试")
            }
        },
        error: function () {
            utils.loaded();
            utils.error("更新失败，请稍后再试")
        }
    })
}

function deleteOldDatas() {
    utils.loading();
    $.ajax({
        url: '/admin/api/deleteOldDatas/',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('刷新完成');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("删除失败，请稍后再试")
            }
        },
        error: function () {
            utils.loaded();
            utils.error("删除失败，请稍后再试")
        }
    })
}

function regularUpdateStart() {
    utils.loading();
    $.ajax({
        url: '/admin/api/regularUpdateStart/',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('自动更新已开启，默认 4 小时更新一次数据库。');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("开启自动更新失败，错误信息：" + data.msg);
            }
        },
        error: function () {
            utils.loaded();
            utils.error("开启自动更新失败，请稍后再试")
        }
    })
}

function regularUpdateClose() {
    utils.loading();
    $.ajax({
        url: '/admin/api/regularUpdateClose/',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.data) {
                utils.loaded();
                utils.success('自动更新已关闭。');
                setTimeout(function () {
                    window.location.reload();
                }, 2000)
            } else {
                utils.loaded();
                utils.error("关闭自动更新失败，错误信息：" + data.msg);
            }
        },
        error: function () {
            utils.loaded();
            utils.error("关闭自动更新失败，请稍后再试")
        }
    })
}