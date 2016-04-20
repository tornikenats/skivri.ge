var monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

window.onload = function () {
    var ctx = document.getElementById("pvChart");
    $.get('/analytics/pageviews')
        .done(function (resp) {
            groups = {};
            resp.pageviews.forEach(function (pageview_date) {
                date_obj = new Date(pageview_date);
                group = new Date(date_obj.getFullYear(), date_obj.getMonth(), date_obj.getDate());
                groups[group] = groups[group] || [];
                groups[group].push(pageview_date);
            });

            labels = Object.keys(groups).map(function (group) {
                date_obj = new Date(group);
                return monthNames[date_obj.getMonth()] + ' ' + date_obj.getDate();
            })
            data = Object.keys(groups).map(function (group) {
                return groups[group].length;
            })

            var pvChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Page views',
                        data: data
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });

        });
};