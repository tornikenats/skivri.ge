var monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

window.onload = function () {
    var dailyChart = c3.generate({
        bindto: '#dailyChart',
        types: {
            Monthly: 'bar'
        },
        data: {
            x: 'labels',
            columns: [['labels'], ['Monthly']],
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
    })


    var hourlyChart = c3.generate({
        bindto: '#hourlyChart',
        data: {
            x: 'labels',
            columns: [['labels'], ['Views']],
        },
        axis: {
            x: {
                type: 'bar',
                tick: {
                    rotate: 75,
                    multiline: false,
                    culling: {
                        max: 7 // the number of tick texts will be adjusted to less than this value
                    }
                },
                height: 100
            }
        },
        legend: {
            show: false
        },
    })

    var start_date = new Date();
    start_date.setDate(start_date.getDate() - 7); // week worth of data
    var end_date = 'newest';

    $.get('/analytics/pageviews?start-date=' + formatDate(start_date) + '&end-date=' + end_date)
    .done(function (resp) {
        var daily_groups = resp['daily_groups'];
        var groups = Object.keys(daily_groups);
        var labels = ['labels'];
        var columns = [];
        var users = _.range(resp['user_count'] + 1);
        _.each(users, function(user){ columns[user] = [] })

        groups.forEach(function(group){
            // create labels
            date_obj = new Date(group);
            labels.push(monthNames[date_obj.getMonth()] + ' ' + date_obj.getDate());

            // create data
            var users_in_group = [];
            // for users in period add their counts
            Object.keys(daily_groups[group]).forEach(function(str_user_id){
                user_id = parseInt(str_user_id);
                columns[user_id].push(daily_groups[group][user_id]);
                users_in_group.push(user_id);
            });
            // for all other users add 0
            users.filter(function(user_id){
                return users_in_group.indexOf(user_id) < 0;
            })
            .forEach(function(user_id){
                columns[user_id].push(0);
            });
        });

        for(i = 0; i < columns.length; i++){
            columns[i].unshift("U"+i);
        };

        dailyChart.groups([columns.map(function(column){return column[0]})]);
        columns.push(labels);

        dailyChart.load({
            columns: columns
        });


    });

    $.get('/analytics/pageviewshourly?start-date=' + formatDate(start_date) + '&end-date=' + end_date)
    .done(function(resp){
        var hourly_groups = resp['hourly_groups'];
        var groups = Object.keys(hourly_groups);
        var start_date = new Date(groups[0]);
        var end_date = new Date(groups[groups.length - 1]);
        var columns = [];

        columns[0] = getDates(start_date, end_date).map(function(date_obj){
            // manualy pad days
            var hours = date_obj.getHours() < 10 ? '0' + date_obj.getHours() : date_obj.getHours();
            var days = date_obj.getDate() < 10 ? '0' + date_obj.getDate() : date_obj.getDate();
            return monthNames[date_obj.getMonth()] + ' ' + days + ', ' + date_obj.getFullYear() + " " + hours + ":00:00";
        });

        columns[1] = [];
        columns[0].map(function(date_str){
            if(hourly_groups[date_str] != undefined){
                columns[1].push(hourly_groups[date_str]);
            }else{
                columns[1].push(0);
            }
        });

        columns[0].splice(0,1,'labels');
        columns[1].splice(0,1,'Views');
        hourlyChart.load({
            columns: columns
        })
    })
};

function getDates(startDate, stopDate) {
    var dateArray = new Array();
    var currentDate = startDate;
    while (currentDate <= stopDate) {
        dateArray.push( new Date (currentDate) )
        currentDate = currentDate.addHours(1);
    }
    return dateArray;
}
