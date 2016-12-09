$(document).ready(function(){
	new WOW().init();

$('#suggestion').keyup(function(){
		var query;
		query = $(this).val();
		$.get('/suggest_category/', {suggestion: query}, function(data){
		$('#cats').html(data);
		});
});


		//like button

		$('#likes').click(function(){
				var cat_id;
				cat_id = $(this).attr("data-catid");

	//Pulls out cat_id ^
				$.get('/like_category/', {category_id: cat_id}, function(data){
						$('#like-count').html(data);
						$('#likes').hide();
				});
		});


		$('#suggestion').keyup(function(){
			var query;
			query = (this).val();
			$.get('/suggest_category/', {suggestion:query}, function(data){
				$('#cats').html(data);
			});
		});

		$('.tutorial-add').click(function(){
			var cat_id = $(this).attr("data-catid");
			var url = $(this).attr("data-url");
			var title = $(this).attr("data-title");
			var user = $(this).attr("data-user");
			var me = $(this)
			console.log('worked')

		$.get('/auto_add_page/', {category_id : cat_id, url : url, title : title, user : user},
			function(data){
								$('#pages').html(data);
								me.hide();
								});
										});
	});



