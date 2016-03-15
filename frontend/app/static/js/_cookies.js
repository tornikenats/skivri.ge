_cookies = function () { }
_cookies.prototype = {
  project_id: 'cis3210-tnatsvli-Qt0sEzGHQQ',
  checkOrMark: function(){
    if(this.readCookie(this.project_id)){
      return true
    }else{
      this.createCookie(this.project_id, '1', 90)
      return false
    }
  },
  createCookie: function (name, value, days) {
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      var expires = "; expires=" + date.toGMTString();
    }
    else var expires = "";
    document.cookie = name + "=" + value + expires + "; path=/";
  },
  readCookie: function (name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  },
  eraseCookie: function (name) {
    createCookie(name, "", -1);
  },
  getAll: function(){
    var ca = document.cookie.split(';');
    var results = []
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') c = c.substring(1, c.length);
      var keyValue = c.split('=')
      results.push({'key':keyValue[0],'value': keyValue[1]})
    }
    return results;
  }
}

var Cookies = new _cookies();
