$(function(){
	var bg = $('#bg').slider()
		.on('change', function(){
			Settings.set('background', 'hsl('+bg.getValue()+', 100%, 50%)')
		})
		.data('slider')
		
	var nav_bg = $('#nav-bg').slider()
		.on('change', function(){
			Settings.set('nav_background', 'hsl('+nav_bg.getValue()+', 100%, 50%)')
		})
		.data('slider')
		
	var fg = $('#fg').slider()
		.on('change', function(){
			Settings.set('color', 'hsl('+fg.getValue()+', 100%, 50%)')
		})
		.data('slider')
	$("*[data-btn='save-prefs']").click(function(){
		Settings.saveAll();
		$('#save-success').removeClass('invisible')
		setTimeout(function(){
			$('#save-success').addClass('invisible')			
		}, 1000)
	})
	
	$("*[data-btn='reset-prefs']").click(function(){
		Settings.reset()
		Settings.saveAll();
	})
})