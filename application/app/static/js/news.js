var language = 'eng';
var page = 1;

$(function () {

    // Get language from url parameter
    params = location.search.substring(1).split("&");
    for(var i = 0; i < params.length; i++) {
        keyval = params[i].split("=");
        if(keyval[0] == "lang") {
            language = keyval[1];
        }
    }

    $("#lang-eng").click(function () {
        language = 'eng';
        updateQueryParams(page, language);
    });

    $("#lang-geo").click(function () {
        language = 'geo';
        updateQueryParams(page, language);
    });

    $(".page-buttons").click(function (e) {
        page = $(e.toElement).attr('data-page');
        updateQueryParams(page, language);
    });

    function updateQueryParams(page, lang) {
        var params = { page: page, lang: lang};
        location = '/news?' + $.param(params);
    }

    $(".article-title").mousedown(function(e){
        b(e.target.id);
    });

});