$(function() {

	$('.add-to-basket').click(function(){
        var price = $(this).data('price')
		$.ajax({
			'url':$(this).data('url'),
			success:function(response){
                if (response.status == "success"){
                    console.log($(this).data('price'));
                	ajax_notification("Product Added To Basket ...", 'success', 3000);
                    $('#basket-price-amount').html(parseInt($('#basket-price-amount').text())+price);
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