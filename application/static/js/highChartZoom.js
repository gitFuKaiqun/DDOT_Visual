/**
 * Created by Kaiqun on 8/6/14.
 */
function generateChart() {
    var TRange = document.getElementById("reservationtime").value;
    var AcisaNo = document.getElementById("slct_acisa").value;

    var urlStr = '/_high_chart?TRange=' + TRange + '&AcisaNo=' + AcisaNo;

    loading_indicator_trigger();
    $.getJSON(urlStr, {}, function(data) {
        HighData = data.result;
        $('#container').highcharts({
            chart: {
                zoomType: 'x'
            },
            title: {
                text: 'Time vs Volume'
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            },
            xAxis: {
                type: 'datetime',
                minRange: 1 * 24 * 3600000 // fourteen days
            },
            yAxis: {
                title: {
                    text: 'Exchange rate'
                }
            },
            legend: {
                enabled: true
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },

            series: HighData
        });

        loading_indicator_trigger();
    });
}
