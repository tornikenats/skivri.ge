(function () {
    var img = new Image,
        url = encodeURIComponent(document.location.href),
        title = encodeURIComponent(document.title),
        ref = encodeURIComponent(document.referrer);
    img.src = '/analytics/a.gif?url=' + url + '&t=' + title + '&ref=' + ref;
})();

function b(i) {
    var img = new Image;
    img.src = '/analytics/b.gif?id=' + i;
}