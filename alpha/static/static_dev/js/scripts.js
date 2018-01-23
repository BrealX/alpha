$(document).ready(function() {
	var form = $('#form-buying-product');
	console.log(form);
	form.on('submit', function(e) {
		e.preventDefault();
		console.log('123');
		var nmb = $('#number').val();
		console.log(nmb);
		var submit_btn = $('#submit_btn');
		var product_id = submit_btn.data('product_id');
		var product_name = submit_btn.data('name');
		var product_price = submit_btn.data('price');
		console.log(product_id);
		console.log(product_name);

			var data = {};
			data.product_id = product_id;
			data.nmb = nmb;
			var csfr_token = $('#form-buying-product [name="csrfmiddlewaretoken"]').val();
			data["csrfmiddlewaretoken"] = csfr_token;

			var url = form.attr("action");
			$.ajax({
				url: url,
				type: 'POST',
				data: data,
				cache: true,
				success: function(data) {
					console.log('OK');
					console.log(data.products_total_nmb)
					if (data.products_total_nmb) {
						$('#basket_total_nmb').text("("+data.products_total_nmb+")");
						console.log(data.products);
						$('.basket-items ul').html('');
						$.each(data.products, function(k, v) {
							$('.basket-items ul').append('<li>' + v.name + ', ' + v.nmb + ' шт. ' + 'по ' + v.price_per_item + ' грн   ' + '</li>');
						})
					}
				},
				error: function() {
					console.log('error');
				}
			})


		$('.basket-items ul').append('<li>' + product_name + ', ' + nmb + ' шт. ' + 'по ' + product_price + ' грн   ' + 
		//'<a class="delete-item" href="">x</a>' + 
		'</li>');
	})

	function showingBasket() {
		$('.basket-items').removeClass('hidden');
	}

	$('.basket-container').on('click', function(e) {
		e.preventDefault();
		showingBasket();
	})

	$('.basket-container').mouseover(function() {
		showingBasket();
	})

	//$('.basket-container').mouseout(function() {
	//	showingBasket();
	//})

	$(document).on('click', '.delete-item', function(e) {
		e.preventDefault();
		$(this).closest('li').remove();
	})
})