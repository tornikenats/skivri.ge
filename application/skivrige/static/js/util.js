// First, checks if it isn't implemented yet.
if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

if (!Number.prototype.formatMoney) {
  Number.prototype.formatMoney = function(c, d, t){
  var n = this, 
      c = isNaN(c = Math.abs(c)) ? 2 : c, 
      d = d == undefined ? "." : d, 
      t = t == undefined ? "," : t, 
      s = n < 0 ? "-" : "", 
      i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", 
      j = (j = i.length) > 3 ? j % 3 : 0;
    return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
  };
}

// returns UTC string
function formatDate(date){
    // YYYY-mm-dd
    return date.toISOString().slice(0, 10);
}

// return UTC string
function formatDateTime(date){
    // YYYY-mm-dd-H-M
    return date.toISOString().slice(0, 10) + '-' + date.getUTCHours() + '-' + date.getUTCMinutes();
}

Date.prototype.addDays = function(days) {
    var dat = new Date(this.valueOf())
    dat.setDate(dat.getDate() + days);
    return dat;
}

Date.prototype.subtractDays = function(days) {
    var dat = new Date(this.valueOf())
    dat.setDate(dat.getDate() - days);
    return dat;
}

Date.prototype.addHours = function(hours){
    var dat = new Date(this.valueOf());
    dat.setTime(dat.getTime() + (hours*60*60*1000));
    return dat;
}

Date.prototype.subtractHours = function(hours){
    var dat = new Date(this.valueOf());
    dat.setTime(dat.getTime() - (hours*60*60*1000));
    return dat;
}