$(function(){
    $("#table-title").hide()

    Charts.createSpinner('chart')

	$.get("newsdesk/items/keywords", {"time-range": 30})
        .done(function(result){
            $('#chart').empty()
            //dataset = []
            //$.each(result, function(i){
            //    dataset.push({subject:result[i][0], count: parseInt(result[i][1])})
            //})

            Charts.createPieChart('chart', result['most-common'], quantitySelector, labelSelector, onSelection)

            $(".search-span").show()
            $(".loading-span").hide()

            function quantitySelector(d){
                return d[1]
            }

            function labelSelector(d){
                return d[0] + " (" + d[1] + ")"
            }

            function onSelection(item){
                $.get("newsdesk/item", {keyword: item[0]})
                    .done(function(result){
                        $("#resultTable").fadeTo(0, 0.33)
                        $("#resultTable").removeClass("invisible")

                        var rows = "";
                        var i = 0;
                        currentArticles = result['article_list'];

                        result['article_list'].map(function (article) {
                            rows += '<tr data-indx="' + (i++) + '"><td>' + article.item_type +
                            '</td><td>' + article.title +
                            '</td><td>' + (article.published_date !== null?article.published_date:'') +
                            '</td><td><a href=\'' + article.url + '\' target=\'_blank\'>NYT Link</a></td></tr>';
                        })
                        if(rows === ""){
                            $("#emptyResult").show();
                        }else{
                            $("#emptyResult").hide();
                            $("#table-title").show();
                        }

                        $('#resultTable > tbody').empty()
                        $('#resultTable > tbody:last-child').append(rows)
                        $('#resultTable').fadeTo(0, 1)
                    })
                    .error(onError)
            }
        })
        .error(onError)

    $( "#articleDialog" ).dialog({
        autoOpen : false, modal : true
    });

    $("#resultTable tbody").on('click', 'tr', function(e){
        var index = parseInt($(this).data('indx'))
        if(currentArticles[index].lead_paragraph === null){
            $("#articleDialog").text("No lead paragraph is avaiable.")
        }else{
            $("#articleDialog").text(currentArticles[index].abstract)
        }
        $('#articleDialog').dialog('option', 'title', currentArticles[index].title);
        $("#articleDialog").dialog('open');
    })
})

function onError(xhr, status, errorText){
    alert(JSON.stringify({"code":xhr.status, "status":status, "errorText": errorText, "responseText": JSON.parse(xhr.responseText)}, null, 2))
}