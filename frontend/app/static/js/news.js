$(function () {
    $("#lang-eng").click(function () {
        setLang('eng')
    })

    $("#lang-geo").click(function () {
        setLang('geo')
    })

    function setLang(lang) {
        location = '/news?lang=' + lang
    }

    $(".page-buttons").click(function (elem) {
        setPage($(elem.toElement).attr('data-page'))
    })

    function setPage(page) {
        url_split = location.href.split('?')
        if (url_split.length == 1) {
            location = '/news?page=' + page
        } else {
            params = url_split[1]
            if (params.indexOf('page') == -1) {
                params += '&page=' + page
            } else {
                params = params.replace(/page=\d*/, 'page=' + page)
            }
            location = '/news?' + params
        }
    }
});