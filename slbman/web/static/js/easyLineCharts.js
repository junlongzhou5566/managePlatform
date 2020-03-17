/**
 * Created by ZhouJunlong on 2018/4/10.
*/
/**
var arrData = [];
var valueData=[];
var myChart = echarts.init(document.getElementById('line-chart'));
var option2line = {
        backgroundColor: '#3c3c3c',
        title: {
            left: 'center',
            text: '出口流量(/M)',
            textStyle: {
                color: 'white'
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: [],
            axisLine: { lineStyle: { color: 'white' } }
        },
        yAxis: {
            type: 'value',
            axisLine: { lineStyle: { color: 'white' } }
        },
        series: [{
            data: [],
            type: 'line',
            areaStyle: {}
        }]
    };
setInterval(function () {

    $.ajax({
        url: "/history_data",
        type: 'GET',
        traditional:true,
        dataType:'JSON',
        success: function(data){
            valueData = [];
            arrData = [];
            for (var i in data){
                data[i] = JSON.parse(data[i]);
                var currentDataValue=data[i]['value'];
                var currentDataClock=data[i]['clock'];
                valueData.push(currentDataValue);
                arrData.push(currentDataClock);

            }
            option2line.series[0].data=valueData;
            option2line.xAxis.data=arrData;
        }});
    myChart.setOption(option2line, true);
},5000);
 */
