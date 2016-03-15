_settings = function(){
	this.defaults = {
		background: "#fff",
		nav_background: "#222",
		color: "#333"
	}
	this.preferences = $.extend({}, this.defaults);
	
	this.custom_apply = {
		background: function(){
			$('body').css('background-color', Settings.preferences.background)
		},
		nav_background: function(){
			$('.navbar').css('background-color', Settings.preferences.nav_background)					
		},
		color: function(){
			$('body').css('color', Settings.preferences.color)			
		}		
	}
}
_settings.prototype = {
	set: function(name, value){
		this.preferences[name] = value;
		this.custom_apply[name]()
	},
	applyAll: function (){
		for(var item in this.custom_apply){
			this.custom_apply[item]()
		}
	},
	initializeSettings: function(defaults){
		for(var item in this.preferences){
			if(!defaults.hasOwnProperty(item)) {
				throw new Error("Settings must include " + item)
			}
		}
		
		this.preferences = defaults;
	},
	saveAll: function (){
		$.ajax({
            url: "/encryptcookie",
            type: "POST",
            data: JSON.stringify(this.preferences),
			contentType: "application/json; charset=utf-8",
        })
		.done(function(response){
			Cookies.createCookie(Cookies.project_id, response.encrypted, 90)
		})
	},
	loadAll: function(){
		var cookieValue = Cookies.readCookie(Cookies.project_id)
		$.ajax({
            url: "/decryptcookie",
            type: "POST",
            data: JSON.stringify(cookieValue),
			contentType: "application/json; charset=utf-8",
        })
		.done(function(response){
			if(response.valid){
				Settings.preferences = JSON.parse(response.cookie) 
				Settings.applyAll()
			}
		})
	},
	reset: function(){
		for(var item in this.defaults){
			this.set(item, this.defaults[item])
		}
	}
}

var Settings = new _settings();