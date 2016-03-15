var currentArticles = [];

$(function () {
    $("*[data-btn='searchNYT']").click(function (e) {
        if($("#NYTKeywords").val() === ""){
            $("#searchArea").addClass("has-error");
            $("#errorMessage").removeClass("gone");
            return;
        }
        
        $("#resultTable").fadeTo(0, 0.33)
        $("#resultTable").removeClass("invisible")
        
        $.get("api/article/search/" + $("#NYTKeywords").val())
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
    })
        
    $("#NYTKeywords").keypress(function(event){
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
    
    $("#useStaticCheckbox input").change(function(){
        if (this.checked) {
            $("#NYTKeywords").prop('disabled', true)
            $("*[data-btn='searchNYT']").prop('disabled', true)
            $("#NYTKeywords").val('')
            
            $("#resultTable").removeClass("invisible")
            $.get("json/sample_response.json")
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
        }else if(!this.checked){
            $("#NYTKeywords").prop('disabled', false)
            $("*[data-btn='searchNYT']").prop('disabled', false)
            
            $('#resultTable > tbody').empty()
            $('#resultTable').addClass('invisible')
        }
    })
    
    function onError(xhr, status, errorText){
        alert(JSON.stringify({"code":xhr.status, "status":status, "errorText": errorText}, null, 2))
    }
});