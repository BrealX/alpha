$(document).ready(function() {
    var header_form = $('#header_form');

    // MiniCart dynamically update (Ajax) after items adding or removing
    function cart_updating(cart_changes) {
        var csfr_token = $('#header_form [name="csrfmiddlewaretoken"]').val();


        // url address where to send POST
        var url = header_form.attr("action");
            
        $.ajax({
            url: url,
            type: 'POST',
            data: {'csrfmiddlewaretoken': csfr_token, 'cart_changes': JSON.stringify(cart_changes)},
            cache: true,
            success: function(data) {
                if (data.products_in_cart_total_qnty) {
                    $('.cart-qnty-subtotal').text('('+data.products_in_cart_total_qnty+')');
                    $('div#minicarttable table tbody, div#collapsed_minicarttable table tbody').html("");                    $('.cart-area table tbody').html("");
                    $.each(data.products_in_cart, function(k, v) {
                        $('div#minicarttable table tbody').append('<tr class=\"miniCartProduct\"><td class=\"miniCartProductThumbnail\" style=\"width: 20%;\"><div><a href=\"/product-land/'+v.id+'\"><img src=\"'+v.image+'\" alt=\"img\" class=\"img-responsive\" width=\"100\"></a></div></td><td style=\"width: 40%;\"><div class=\"miniCartDescription\"><h4><a href=\"/product-land/'+v.id+'\">'+v.name+'</a></h4><span>'+v.price+' грн.</span></div></td><td class=\"miniCartQuantity\" style=\"width: 10%;\"><a>* '+v.qnty+' шт.</a></td><td class=\"miniCartSubtotal\" style=\"width: 15%;\"><span class="minicart-item-overall price">'+parseFloat(v.total_price).toFixed(2)+' грн.</span></td><td class=\"delete\" style=\"width: 5%;\"><a class=\"delete-item\" href=\"\" data-product_id=\"'+v.id+'\"><i class=\"ion-ios-trash-outline\" style=\"font-size: 30px;\"></i></a></td></tr>');
                        $('div#collapsed_minicarttable table tbody').append('<tr class=\"miniCartProduct\"><td class=\"miniCartProductThumbnail\" style=\"width: 20%;\"><div><a href=\"/product-land/'+v.id+'\"><img src=\"'+v.image+'\" alt=\"img\" class=\"img-responsive\" width=\"100\"></a></div></td><td style=\"width: 40%;\"><div class=\"miniCartDescription\"><h4><a href=\"/product-land/'+v.id+'\">'+v.name+'</a></h4><span>'+v.price+' грн.</span></div></td><td class=\"miniCartQuantity\" style=\"width: 10%;\"><a>* '+v.qnty+' шт.</a></td><td class=\"miniCartSubtotal\" style=\"width: 15%;\"><span class="collapsed-minicart-item-overall price">'+parseFloat(v.total_price).toFixed(2)+' грн.</span></td><td class=\"delete\" style=\"width: 5%;\"><a class=\"delete-item\" href=\"\" data-product_id=\"'+v.id+'\"><i class=\"ion-ios-trash-outline\" style=\"font-size: 30px;\"></i></a></td></tr>');
                        $('div.cart-area table tbody').append('<tr class=\"CartProduct\"><td class=\"CartProductThumbnail\" style=\"width: 20%;\"><div><a href=\"/product-land/'+v.id+'\"><img src=\"'+v.image+'\" alt=\"img\" class=\"img-responsive\" width=\"100\"></a></div></td><td style=\"width: 40%;\"><div class=\"CartDescription\"><h4><a href=\"/product-land/'+v.id+'\">'+v.name+'</a></h4><span class=\"cart-item-price\">'+v.price+'</span><span> грн.</span></div></td><td class=\"CartQuantity\" style=\"width: 15%;\"><input class=\"cart-touchspin form-control\" name=\"cart_touchspin\" type=\"text\" value=\"'+v.qnty+'\" data-product_id=\"'+v.id+'\"></td><td class=\"CartSubtotal\" style=\"width: 15%;\"><span class=\"cart-item-overall price\">'+parseFloat(v.total_price).toFixed(2)+' грн.</span></td><td class=\"delete\" style=\"width: 5%;\"><a href=\"\" class=\"delete-item\" data-product_id=\"'+v.id+'\"><i class=\"ion-ios-trash-outline\" style=\"font-size: 30px;\"></i></a></td></tr>')
                    });
                }
                else if (data.products_in_cart_total_qnty == 0) {
                    $('.cart-qnty-subtotal').text('(0)');
                    $('div#minicarttable table tbody, div#collapsed_minicarttable table tbody, .cart-area table tbody').html("");
                    $('div#minicarttable table tbody, div#collapsed_minicarttable table tbody').append('<div class=\"text-center\"><p class=\"empty-cart\">Ваша корзина пуста. Чтобы оформить заказ, необходимо добавить товар!</p></div>');
                    $('.cart-area table tbody').append('<div class=\"text-center\"><p class=\"empty-cart" style=\"font-size: 40px;\">Ваша корзина пуста. Чтобы оформить заказ, необходимо добавить товар!</p></div>');
                };
                calculatingTotalCartSum();
                $('.cart-touchspin').TouchSpin({ min: 1, step: 1, });
            },
            error: function() {
                console.log('There is an error while Ajax proccessing')
            }
        });
        };

    // Adding single product item to cart from Home Page slider or Landing Page buttons
    function single_adding(button) {
        var button = button;
        var cart_changes = {};
        var product_id = button.data('product_id');
        var qnty = button.data('qnty');
        cart_changes[product_id] = {qnty: qnty, is_delete: false};

        cart_updating(cart_changes);
    };


    // Get data from Product Landing Page Form
    $('button.landing-submit, #landing_page_submit_btn').on('click', function (e) {
        e.preventDefault();
        button = $(this);
        single_adding(button);
    });

    // Get data from Home Page slider buttons
    $('div.action-control').on('click', 'button[id^="main_page_submit_id"]', function (e) {
        e.preventDefault();
        button = $(this);
        single_adding(button);
    });

    // Delete items from miniCart
    $('div.minicart-button').on('click', 'a.delete-item', function(e) {
        e.preventDefault();
        var cart_changes = {};
        product_id = $(this).data("product_id");
        qnty = 0;
        cart_changes[product_id] = {qnty: qnty, is_delete: true};
    
        cart_updating(cart_changes);
	});

    // Changes product in cart quantity with touchspin plugin
    $('#checkout_page_submit').on('click', function() {
        var inputs = $('.cart-touchspin');
        var cart_changes = {};
        for(var i = 0; i < inputs.length; i++) {
            product_id = $(inputs[i]).data('product_id');
            qnty = parseInt($(inputs[i]).val());
            cart_changes[product_id] = {qnty: qnty, is_delete: false};
        }
        cart_updating(cart_changes);
    });

    // Delete items from cart
    $('.cart-area').on('click', 'a.delete-item', function(e) {
        e.preventDefault();
        var cart_changes = {};
        product_id = $(this).data("product_id");
        qnty = 0;
        cart_changes[product_id] = {qnty: qnty, is_delete: true};
        
        cart_updating(cart_changes);
    });
    
    // Shows Cart subtotal (at miniCart dropdown and Cart Page)
    function calculatingTotalCartSum(){
        var minicart_overall = 0;
        var collapsed_minicart_overall = 0;
        var cart_overall = 0;
        $(".minicart-item-overall").each(function(){
            minicart_overall += parseFloat($(this).text());
        });
        $(".collapsed-minicart-item-overall").each(function(){
            collapsed_minicart_overall += parseFloat($(this).text());
        });
        $(".cart-item-overall").each(function(){
            cart_overall += parseFloat($(this).text());
        });
        $('#minicart_subtotal').text(minicart_overall.toFixed(2) + ' грн.');
        $('#collapsed_minicart_subtotal').text(collapsed_minicart_overall.toFixed(2) + ' грн.');
        $('#cart_subtotal').text('Ваш заказ на сумму: '+ cart_overall.toFixed(2) + ' грн.');
    };

    
    // Checks any quantity changes at Cart Page and make changes at Client side
    $(document).on('change', '.cart-touchspin', function(){
        var current_qnty = $(this).val();
        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.cart-item-price').text()).toFixed(2);
        var item_subtotal = parseFloat(current_qnty*current_price).toFixed(2);
        current_tr.find('.cart-item-overall').text(item_subtotal+" грн.");

        calculatingTotalCartSum()
    });

    calculatingTotalCartSum();

    // AOS Animation Initializer
    // https://github.com/michalsnik/aos
    // https://michalsnik.github.io/aos/
    AOS.init();

    // jQuery-ScrollUp Plugin Initializer
    $(function () {
        $.scrollUp({
            scrollText: '<i class="ion-chevron-up"></i>', // Text for element
        });
    });

    // Ajax request for chained select Areas/Cities at /orders/checkout1 page
    $('select#id_anonymous_area, select#id_delivery_area').on('change', function() {
        var area_id = $(this).val();
        $.ajax({
            type: 'get',
            url: '/ajax/get_chained_cities/',
            data: { 'area_id': area_id },
            cache: true,
            success: function(response) {
                $('select#id_anonymous_city, select#id_delivery_city').prop('disabled', false); // Enables element
                $('select#id_anonymous_city, select#id_delivery_city').html("");
                var new_options = response.cities;
                $.each(new_options, function(key, value) {
                    $.each(value, function(k, v) {
                        $('select#id_anonymous_city, select#id_delivery_city').append(
                        $('<option>', { value: k }).text(v));
                    });
                });
            }
        });
    });
});