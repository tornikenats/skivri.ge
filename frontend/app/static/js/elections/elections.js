$(function(){
    cycle = null
    
	$("*[data-btn='searchNYT']").click(function (e) {
        if($("#NYTElectionsText").val() === ""){
            $("#searchArea").addClass("has-error");
            $("#errorMessage").removeClass("gone");
            return;
        }
        
        $("#resultTable").fadeTo(0, 0.33)
        $("#resultTable").removeClass("invisible")
        
		total_contrib = []
		
        $(".search-span").hide()
        $(".loading-span").show()
        
        cycle = $("#NYTElectionsText").val()
        
        $.get("elections/totals/" + cycle)
        .done(function(result){
            $('#chart').empty()
            $.each(result.results, function(i){
                total_contrib.push({'name': result.results[i].candidate_name, 'amt': result.results[i].total_contributions})
            })
            Charts.createPieChart('chart', total_contrib, valueGetter, lableGetter, candidateSelected)
            
            $(".search-span").show()
            $(".loading-span").hide()

            function valueGetter(d){
                return d.amt
            }

            function lableGetter(d){
                return d.name + " raised ${0}".format(parseInt(d.amt).formatMoney(2))
            }

            function candidateSelected(item){
                $.get("api/article/search/" + item.name)
                .done(function(result){
                    var rows = "";
                    currentArticles = result.response.docs;
                    var i = 0;
                    result.response.docs.map(function (article) {
                        rows += '<tr data-indx="' + (i++) + '"><td>' + article.type_of_material +
                        '</td><td>' + article.headline.main +
                        '</td><td>' + (article.pub_date !== null?article.pub_date:'') + '</td></tr>';
                    })
                    if(rows === ""){
                        $("#emptyResult").show();
                    }else{
                        $("#emptyResult").hide();
                    }

                    $('#resultTable > tbody').empty()
                    $('#resultTable > tbody:last-child').append(rows)
                    $('#resultTable').fadeTo(0, 1)
                })
                .error(onError)
            }
        })
        .error(onError)
    })
    
    $("#NYTElectionsText").keypress(function(event){
        if($("#searchArea").hasClass("has-error")){
            $("#searchArea").removeClass("has-error")
            $("#errorMessage").addClass("gone");
        }
        
        if(event.keyCode == 13){
            $("*[data-btn='searchNYT']").click()
        }  
    })
    
    $( "#articleDialog" ).dialog({
        autoOpen : false, modal : true
    });
    
    $("#resultTable tbody").on('click', 'tr', function(e){
        var index = parseInt($(this).data('indx'))
        if(currentArticles[index].lead_paragraph === null){
            $("#articleDialog").text("No lead paragraph is avaiable.")            
        }else{
            $("#articleDialog").text(currentArticles[index].lead_paragraph)
        }
        $('#articleDialog').dialog('option', 'title', currentArticles[index].headline.main);
        $("#articleDialog").dialog('open');
    })

})

function onError(xhr, status, errorText){
    alert(JSON.stringify({"code":xhr.status, "status":status, "errorText": errorText, "responseText": JSON.parse(xhr.responseText)}, null, 2))
}