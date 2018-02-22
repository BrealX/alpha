$(document).ready(function() {
    var product_page_form = $('#product_page_form');
    var navbar_form = $('#navbar_form');

    // MiniCart dynamically update (Ajax) after items adding or removing
    function cart_updating(product_id, qnty, is_delete) {
        var data = {};
        data.product_id = product_id;
        data.qnty = qnty;
        var csfr_token = $('#navbar_form [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csfr_token;

        if (is_delete){
            data['is_delete'] = true;
        }

        // url address where to send POST
        var url = navbar_form.attr("action");
            
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function(data) {
                if (data.products_in_cart_total_qnty) {
                    $('#cart_qnty_subtotal').text('('+data.products_in_cart_total_qnty+')');
                    $('.droppingbasket div.miniCartTable div div table tbody').html("");
                    $.each(data.products, function(k, v) {
                        $('.droppingbasket div.miniCartTable div div table tbody').append('<tr class=\"miniCartProduct\">\
                            <td class=\"miniCartProductThumb\" style=\"width: 20%;\">\
                            <div>\
                            <a href=\"/product/'+v.id+'\">\
                            <img src=\"'+v.image+'\" alt=\"img\"></a>\
                            </div>\
                            </td><td style=\"width: 30%;\">\
                            <div class=\"miniCartDescription\">\
                            <h4><a href=\"/product/'+v.id+'\">'+v.name+'</a></h4>\
                            <div class=\"price\">\
                            <span>'+v.price_per_item+'</span></div>\
                            </div>\
                            </td>\
                            <td class=\"miniCartQuantity\" style=\"width: 13%;\">\
                            <a>* '+v.qnty+' шт.</a></td>\
                            <td class=\"miniCartSubtotal\" style=\"width: 20%;\">\
                            <span>'+parseFloat(v.total_price).toFixed(2)+' UAH</span></td>\
                            <td class=\"delete\" style=\"width: 5%;\"><a class=\"delete-item\" href=\"\" data-product_id=\"'+v.id+'\">x</a>\
                            </td></tr>')
                    });
                }
                else if (data.products_in_cart_total_qnty == 0) {
                    $('#cart_qnty_subtotal').text('(0)');
                    $('.droppingbasket div.miniCartTable div div table tbody').html("");
                    $('.droppingbasket div.miniCartTable div div table tbody').append(
                        '<p class="lead text-center">\
                        ... В Вашей корзине еще нет товаров ...\
                        </p>'
                        );
                };
                    
            },
            error: function() {
                    console.log('some error');
            }
        });
        };


    // Get data from Product Page Form
    product_page_form.on('submit', function(e) {
        e.preventDefault();
        var qnty = $('#product_page_qnty').val();
        var submit_btn = $('#product_page_submit_btn');
        var product_id = submit_btn.data('product_id');
        var product_name = submit_btn.data('name');
        var product_price = submit_btn.data('price');
        var product_total_price = qnty*product_price;
        var product_image = submit_btn.data('image');

        cart_updating(product_id, qnty, is_delete=false);
    });


    // Get data from Main Page Add-to-cart buttons
    $('div.action-control').on('click', 'button[id^="main_page_submit_id"]', function (e) {
        button = $(this)
        e.preventDefault();
        var qnty = button.data('qnty');
        var product_id = button.data('product_id');
        var product_name = button.data('name');
        var product_price = button.data('price');
        var product_total_price = qnty*product_price;
        var product_image = button.data('image');

        cart_updating(product_id, qnty, is_delete=false)
    });

    
    // Cart refreshing while Checkout Page touchspin is activated (only after Refresh button is pressed)
    $('.product-in-cart-qnty').each(function(input) {
    	var checkout_page_input = $(this);
    	var start_checkout_input = parseInt(checkout_page_input.attr('value'));
    	$('div.cartFooter').on('click', '#cart_refresh', function(e) {
        	e.preventDefault();
        	var current_checkout_input = parseInt(checkout_page_input.val());
    		var qnty = current_checkout_input-start_checkout_input;
    		var product_id = checkout_page_input.data('product_id');

    		if (qnty != 0) {
    			cart_updating(product_id, qnty, is_delete=false);
    		};
    		start_checkout_input = current_checkout_input;
    	});
    });


    // Hide success div (Checkout page footer)
    function hideCartFooterDiv() {
    	$('div.box-footer div.pull-left').delay(10000).fadeOut();
    };


    // Show success div when AJAX is OK during cart products adding or removing
    $(document).ajaxSuccess(function(event, request, settings) {
    	element = $('.box-footer').children('.pull-left')
    	if (!element.is(':visible')) {
    		element.attr('style', 'display: visible');
    		hideCartFooterDiv();
    	};
    });
    

    // Open dropdown menu at Navbar
    function showingMenu() {
        $('.dropdown-menu').toggleClass('hidden');
    };

    $('.dropmenu').mouseover(function() {
        showingMenu();
    });

    $('.dropmenu').mouseout(function() {
        showingMenu();
    });

    
    // Opening dropdown cart menu at RightNavbar
    function showingBasket() {
        $('.droppingbasket').toggleClass('hidden');
    };

    $('.basket-container').on('click', function() {
        showingBasket();
    });

    /*$('.basket-container').mouseover(function() {
        showingBasket();
    });

    $('.basket-container').mouseout(function() {
        showingBasket();
    });*/


    // Delete items from miniCart
    $('div.cartMenu').on('click', 'a.delete-item', function(e) {
        e.preventDefault();
        product_id = $(this).data("product_id");
        qnty = 0;
    
        cart_updating(product_id, qnty, is_delete=true)
	});

    $('div.cartContent').on('click', 'a.delete-item', function(e) {
        e.preventDefault();
        product_id = $(this).data("product_id");
        qnty = 0;
        
        cart_updating(product_id, qnty, is_delete=true)
	});

    
    // Show Cart subtotal (at miniCart dropdown & Checkout Page Right Bar)
    function calculatingTotalBasketAmount(){
        var total_price = 0
        $(".total-product-in-cart-sum").each(function(){
            total_price += parseFloat($(this).text());
        });
        $('#total_price, #miniCart_subtotal').text(total_price.toFixed(2) + ' UAH');
    };

    
    // Check any quantity changes at Cart Page and make changes to Cart
    $(document).on('change', '.product-in-cart-qnty', function(){
        var current_qnty = $(this).val();
        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-in-basket-price').text()).toFixed(2);
        var total_amount = parseFloat(current_qnty*current_price).toFixed(2);
        current_tr.find('.total-product-in-cart-sum').text(total_amount);

        calculatingTotalBasketAmount();
    });

    calculatingTotalBasketAmount();


    // Home Page Slider Initializer
    $('.owl-carousel').owlCarousel({
    loop:true,
    margin:25,
    nav:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:3
        },
        1000:{
            items:4
        }
    }
    });


    // Add to Wishlist Click Event
    $('.add-fav').click(function (e) {
        e.preventDefault();
        $(this).addClass("active"); // ADD TO WISH LIST BUTTON 
        $(this).attr('data-original-title', 'Понравилось');// Change Tooltip text
    });


    // Product Page Zoomer Initializer
    $(window).on('load', function() {
        $('.sp-wrap').smoothproducts();
    }); 


    // Bootstrap Touchspin at Cart Page Initializer
    $(window).on('load', function() {
        $("input[name='quanitySniper']").TouchSpin();
    });

    // ICheck Initializer
    // https://github.com/fronteed/iCheck/
    $('input').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
        increaseArea: '20%' // optional
    });

    // Select2 Initializer
    // https://select2.org/getting-started/basic-usage
    //$('.js-example-basic-single').select2();
    //$('.django-select2').djangoSelect2();

    // My Profile Page address delete button
    $('#my_profile_address_delete').on('click', function(e) {
        e.preventDefault();
        var address_delete_form = $('#my_profile_address_delete_form');
        var url = address_delete_form.attr('action');
        var csfr_token = $('#my_profile_address_delete_form [name="csrfmiddlewaretoken"]').val();
        data = {}
        data["csrfmiddlewaretoken"] = csfr_token;
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function(data) {
                if (!data.profile_delivery_address) {
                    $('.address-line').html("");
                    $('.address-line').text("Вы не указали адрес доставки");
                };
            }
        });
    });

    // My Profile Page Personal delete button
    $('#my_personal_delete').on('click', function(e) {
        e.preventDefault();
        var personal_delete_form = $('#my_personal_delete_form');
        var url = personal_delete_form.attr('action');
        var csfr_token = $('#my_personal_delete_form [name="csrfmiddlewaretoken"]').val();
        data = {}
        data["csrfmiddlewaretoken"] = csfr_token;
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function(data) {
                if (!data.user_firstname && !data.profile_phone) {
                    $('.profile-firstname').html("");
                    $('.profile-phone').html("");
                    $('.profile-firstname').text("Вы не указали имя");
                    $('.profile-phone').text("Вы не указали контактный номер телефона");
                };
            }
        });
    });

    // Modal window on account deletion (delete confirmation & delete process)
    $('div#deleteModalCenter').on('show.bs.modal', function(e) {
        $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
    });
    $('div#deleteModalCenter').on('click', '.btn-ok', function(e) {
        e.preventDefault();
        var account_delete_form = $('#my_account_delete_form');
        var url = account_delete_form.attr('action');
        var go_home_form = $('#go_home_form');
        var redirect_url = go_home_form.attr('action');
        var csfr_token = $('#my_account_delete_form [name="csrfmiddlewaretoken"]').val();
        data = {}
        data["csrfmiddlewaretoken"] = csfr_token;
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function(data) {
                window.location.href = redirect_url;
            }
        })
    });

    // Ajax request to /ajax/get_cities/ for Delivery Auto cities API
    $('select#id_anonymous_area').on('change', function() {
        var area_id = $(this).val();
        $.ajax({
            type: 'get',
            url: '/ajax/get_cities/',
            data: { 'area_id': area_id },
            cache: true,
            success: function(response) {
                $('select#id_anonymous_city').prop('disabled', false); // Enables element
                $('select#id_anonymous_city').html("");
                var new_options = response.cities;
                $.each(new_options, function(key, value) {
                    $.each(value, function(k, v) {
                        $('select#id_anonymous_city').append(
                        $('<option>', { value: k }).text(v));
                    });
                });
            }
        });
    });

    // 

});


