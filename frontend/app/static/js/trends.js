var dailyChart = c3.generate({
        bindto: '#trendsChart',
        types: {
            Monthly: 'bar'
        },
        data: {
            x: 'labels',
            columns: [['labels'], ['counts']],
            type: 'bar',
        },
        axis: {
            x: {
                type: 'category',
                tick: {
                    rotate: 75,
                    multiline: false
                },
                height: 80
            }
        },
        legend: {
            //show: false
        },
        tooltip: {
            grouped: false
        }
    });

$("#getTrends").click(function(){
    var start_date = new Date();
    var end_date = new Date();
    switch($('#Period').prop('selectedIndex')){
        case 0:
            start_date = start_date.subtractHours(1);
            break;
        case 1:
            start_date = start_date.subtractHours(2);
            break;
        case 2:
            start_date = start_date.subtractDays(1);
            break;
        case 3:
            start_date = start_date.subtractDays(7);
            break;
    }

    $.get('/trends/stats?start-date=' + formatDateTime(start_date) + '&end-date=' + formatDateTime(end_date))
    .done(function (resp) {

        var labels_arr = ['labels'];
        var data_arr = ['counts'];

        _.each(resp['trends'], function(trend_pair){
            labels_arr.push(trend_pair[0]);
            data_arr.push(trend_pair[1]);
        });

        dailyChart.load({
            columns: [labels_arr, data_arr]
        });
    });
});

