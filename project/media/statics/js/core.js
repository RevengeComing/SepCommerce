$(function() {

	$('.add-to-basket').click(function(){
		$.ajax({
			'url':$(this).data('url'),
			success:function(response){
                if (response == "success"){
                	ajax_notification("Product Added To Basket ...", 'success', 3000)
                }
            },
            start:function(){
            	ajax_notification("Waiting ...", 'info')
            }
		});
	});

});

function update_basket() {

}

function ajax_notification(msg,type,time){
    $('#notification').removeClass().addClass('alert-' + type).html(msg).fadeIn();
    if (time) {
        setTimeout(function() {
            $('#notification').fadeOut();
        }, time);
    }
}