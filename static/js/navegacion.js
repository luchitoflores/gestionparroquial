define(['jquery', 'modernizr'], function($,Modernizr) {
	if(!Modernizr.inputtypes.date){
		console.log('no poseo esa propiedad');
		$('input[type=date]').datepicker({
			format: 'yyyy-mm-dd'
		}); 
	} 
	if(!Modernizr.inputtypes.time){
		console.log('no poseo esa propiedad time');
		$('input[type=time]').timepicker({
			defaultTime: false,
			showMeridian: false,
			format: 'HH:mm:ss'
			//showSeconds: true,
		}); 
	}
	return window.Modernizr 
});