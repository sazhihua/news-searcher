$(function () {
    // function_1();
    // function_2();
    function_3();
    function_4();
    // function_5();
})

function function_1() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('zhuzhuangtu'), 'macarons');
    // 指定图表的配置项和数据
    var option = {
        title: {
            text: '网站统计测试图',
            left: 'center',
            top: 10,
            textStyle: {
                color: 'white'
            }
        },
        tooltip: {},
        // legend: {
        //     data: ['销量']
        // },
        xAxis: {
            type: 'category',
            data: ['新浪新闻', '央视网', '测试专用', '搜狐', '人民日报'],
            axisLabel: {
                textStyle: {
                    color: 'white',//坐标值得具体的颜色
                }
            }
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                textStyle: {
                    color: 'white',//坐标值得具体的颜色
                }
            }
        },
        series: [
            {
                type: 'bar',
                data: [{value: 500, itemStyle: {color: 'white',}}, 202, 360, 108, 180]
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

function function_2() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('bingtu'), 'macarons');
    // 指定图表的配置项和数据
    var option = {
        title: {
            text: '类别统计测试图',
            left: 'center',
            top: 10,
            textStyle: {
                color: 'white'
            }
        },
        tooltip: {
            trigger: 'item',
        },
        legend: {
            bottom: '5%',
            left: 'center',
            textStyle: {
                color: 'white',
            }
        },
        series: [
            {
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                // label: {
                //     show: true,
                //     position: 'center'
                // },
                emphasis: {
                    label: {
                        show: true,
                    }
                },
                labelLine: {
                    show: true
                },
                data: [
                    {value: 1048, name: '国内'},
                    {value: 735, name: '国外'},
                    {value: 580, name: '财经'},
                    {value: 484, name: '体育'},
                    {value: 300, name: '娱乐'}
                ]
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

function function_3() {
    // 初始化echarts实例
    var myEcharts = echarts.init(document.getElementById("ditu"), 'shine');
    var option = {
        title: {  //标题样式
            text: '中国地图',
            left: "center",
            top: 10,
            textStyle: {
                fontSize: 18,
                color: 'white'
            },
        },
        tooltip: {  //这里设置提示框
            trigger: 'item',  //数据项图形触发
            backgroundColor: "white",  //提示框浮层的背景颜色。
            //字符串模板(地图): {a}（系列名称），{b}（区域名称），{c}（合并数值）,{d}（无）
            formatter: function (val) {
                if (val.value) {
                    return `<a href='#'>测试</a>${val.name}<br/>查询次数：${val.value}，手机：222，电脑：333`
                } else {
                    return `地区：${val.name}<br/>查询次数：0`
                }
            }
            // '地区：{b}<br/>查询次数：{c}'
        },
        visualMap: {//视觉映射组件
            top: 'center',
            left: 'left',
            min: 0,
            max: 100000,
            text: ['最高', '最低'],
            realtime: false,  //拖拽时，是否实时更新
            calculable: false,  //是否显示拖拽用的手柄
            inRange: {
                // color: ['lightskyblue', 'yellow', 'orangered']
                color: [
                    '#313695',
                    '#4575b4',
                    '#74add1',
                    '#abd9e9',
                    '#e0f3f8',
                    '#ffffbf',
                    // '#fee090',
                    // '#fdae61',
                    // '#f46d43',
                    // '#d73027',
                    // '#a50026'
                ]
            },
            textStyle: {
                color: 'white'
            }
        },
        series: [
            {
                name: '查询次数',
                type: 'map',
                mapType: 'china',
                roam: false,//是否开启鼠标缩放和平移漫游
                itemStyle: {//地图区域的多边形 图形样式
                    normal: {//是图形在默认状态下的样式
                        label: {
                            show: false,//是否显示标签
                        }
                    },
                    zoom: 1,  //地图缩放比例,默认为1
                    emphasis: {//是图形在高亮状态下的样式,比如在鼠标悬浮或者图例联动高亮时
                        label: {
                            show: true,
                            textStyle: {
                                color: 'white',
                            }
                        },
                    }
                },
                top: "3%",//组件距离容器的距离
                data: [
                    {name: '北京', value: 350000},
                    {name: '天津', value: 120000},
                    {name: '上海', value: 300000},
                    {name: '重庆', value: 92000},
                    {name: '河北', value: 25000},
                    {name: '河南', value: 20000},
                    {name: '云南', value: 500},
                    {name: '辽宁', value: 3050},
                    {name: '黑龙江', value: 80000},
                    {name: '湖南', value: 2000},
                    {name: '安徽', value: 24580},
                    {name: '山东', value: 40629},
                    {name: '新疆', value: 36981},
                    {name: '江苏', value: 13569},
                    {name: '浙江', value: 24956},
                    {name: '江西', value: 15194},
                    {name: '湖北', value: 41398},
                    {name: '广西', value: 41150},
                    {name: '甘肃', value: 17630},
                    {name: '山西', value: 27370},
                    {name: '内蒙古', value: 27370},
                    {name: '陕西', value: 97208},
                    {name: '吉林', value: 88290},
                    {name: '福建', value: 19978},
                    {name: '贵州', value: 94485},
                    {name: '广东', value: 89426},
                    {name: '青海', value: 35484},
                    {name: '西藏', value: 97413},
                    {name: '四川', value: 54161},
                    {name: '宁夏', value: 56515},
                    {name: '海南', value: 54871},
                    // { name: '台湾', value: 48544 },
                    {name: '香港', value: 49474},
                    {name: '澳门', value: 34594}
                ]
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myEcharts.setOption(option);
}

function function_4() {
    let temp = `<div class="vertical-custom">
        <span class="text-center">搜索情况统计</span>
        <table class="table table-custom">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">First</th>
                    <th scope="col">Last</th>
                    <th scope="col">Handle</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <th scope="row">1</th>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                </tr>
                <tr>
                    <th scope="row">2</th>
                    <td>Jacob</td>
                    <td>Thornton</td>
                    <td>@fat</td>
                </tr>
                <tr>
                    <th scope="row">3</th>
                    <td colspan="2">Larry the Bird</td>
                    <td>@twitter</td>
                </tr>
            </tbody>
        </table></div>
    `
    $('#biaoge_1').html(temp)
}

function function_5() {
    let temp = `<div class="vertical-custom">
        <span>更新情况统计</span>
        <table class="table table-custom">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">First</th>
                    <th scope="col">Last</th>
                    <th scope="col">Handle</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <th scope="row">1</th>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                </tr>
                <tr>
                    <th scope="row">2</th>
                    <td>Jacob</td>
                    <td>Thornton</td>
                    <td>@fat</td>
                </tr>
                <tr>
                    <th scope="row">3</th>
                    <td colspan="2">Larry the Bird</td>
                    <td>@twitter</td>
                </tr>
            </tbody>
        </table></div>
    `
    $('#biaoge_2').html(temp)
}