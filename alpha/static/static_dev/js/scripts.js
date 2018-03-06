$(document).ready(function() {
    var header_form = $('#header_form');

    // MiniCart dynamically update (Ajax) after items adding or removing
    function cart_updating(product_id, qnty, is_delete) {
        var data = {};
        data.product_id = product_id;
        data.qnty = qnty;
        var csfr_token = $('#header_form [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csfr_token;

        if (is_delete){
            data['is_delete'] = true;
        }

        // url address where to send POST
        var url = header_form.attr("action");
            
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function(data) {
                if (data.products_in_cart_total_qnty) {
                    $('#cart_qnty_subtotal').text('('+data.products_in_cart_total_qnty+')');
                    $('.dropcart div.minicarttable table tbody').html("");
                    $.each(data.products, function(k, v) {
                        $('.dropcart div.minicarttable table tbody').append('<tr class=\"miniCartProduct\"><td class=\"miniCartProductThumbnail\" style=\"width: 20%;\"><div><a href=\"/product/'+v.id+'\"><img src=\"'+v.image+'\" alt=\"img\" class=\"img-responsive\" width=\"100\"></a></div></td><td style=\"width: 40%;\"><div class=\"miniCartDescription\"><h4><a href=\"/product/'+v.id+'\">'+v.name+'</a></h4><span>'+v.price_per_item+' грн.</span></div></td><td class=\"miniCartQuantity\" style=\"width: 10%;\"><a>* '+v.qnty+' шт.</a></td><td class=\"miniCartSubtotal\" style=\"width: 15%;\"><span class="minicart-item-overall price">'+parseFloat(v.total_price).toFixed(2)+' грн.</span></td><td class=\"delete\" style=\"width: 5%;\"><a class=\"delete-item\" href=\"\" data-product_id=\"'+v.id+'\">x</a></td></tr>')
                    });
                }
                else if (data.products_in_cart_total_qnty == 0) {
                    $('#cart_qnty_subtotal').text('(0)');
                    $('.dropcart div.minicarttable table tbody').html("");
                    $('.dropcart div.minicarttable table tbody').append('<p class="lead text-center">... В Вашей корзине еще нет товаров ...</p>');
                };
                calculatingTotalCartSum();
                    
            },
            error: function() {
                    console.log('some error');
            }
        });
        };


    /*// Get data from Product Page Form
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
    });*/

    // Get data from Product Landing Page Form
    $('button.landing-submit').on('click', function (e) {
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

    // Get data from Home Page slider buttons
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

    
    /*// Cart refreshing while Checkout Page touchspin is activated (only after Refresh button is pressed)
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
    });*/


    /*// Hide success div (Checkout page footer)
    function hideCartFooterDiv() {
    	$('div.box-footer div.pull-left').delay(10000).fadeOut();
    };*/


    /*// Show success div when AJAX is OK during cart products adding or deleting
    $(document).ajaxSuccess(function(event, request, settings) {
    	element = $('.box-footer').children('.pull-left')
    	if (!element.is(':visible')) {
    		element.attr('style', 'display: visible');
    		hideCartFooterDiv();
    	};
    });*/

    // Delete items from miniCart
    $('div.minicart-button').on('click', 'a.delete-item', function(e) {
        e.preventDefault();
        product_id = $(this).data("product_id");
        qnty = 0;
    
        cart_updating(product_id, qnty, is_delete=true)
	});

    // Delete items from Checkout Page
    $('.cart-area').on('click', 'a.delete-item', function(e) {
        e.preventDefault();
        product_id = $(this).data("product_id");
        qnty = 0;
        
        cart_updating(product_id, qnty, is_delete=true)
	});

    
    // Shows Cart subtotal (at miniCart dropdown and Cart Page)
    function calculatingTotalCartSum(){
        var minicart_overall = 0;
        var cart_overall = 0;
        $(".minicart-item-overall").each(function(){
            minicart_overall += parseFloat($(this).text());
        });
        $(".cart-item-overall").each(function(){
            cart_overall += parseFloat($(this).text());
        });
        console.log(minicart_overall);
        $('#miniCart_subtotal').text(minicart_overall.toFixed(2) + ' грн.');
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

    // CountTo Plugin Initializer (https://stackoverflow.com/questions/43202706/jquery-counto-js-on-scroll-count-numbers-not-onload)
    /*function isScrolledIntoView(el) {
        if (el.getBoundingClientRect().top | el.getBoundingClientRect().bottom) { 
            var elemTop = el.getBoundingClientRect().top;
            var elemBottom = el.getBoundingClientRect().bottom;

            var isVisible = (elemTop >= 0) && (elemBottom <= window.innerHeight);
            return isVisible;
        $(window).on('scroll', function() {
            if (isScrolledIntoView(document.getElementById('counters'))) {
                $('.counter').countTo();
                $('.counter-decimal').countTo({
                    formatter: function (value, options) {
                        return value.toFixed(1);
                    }
                });
            // Unbind scroll event
            $(window).off('scroll');
            }
        });
    }};*/
    $('.counter').countTo();
    $('.counter-decimal').countTo({
        formatter: function (value, options) {
            return value.toFixed(1);
        }
    });


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

    // Home Page Slider Initializer
    $('.owl-carousel').owlCarousel({
    loop:true,
    margin:25,
    nav:false,
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
    $('.cart-touchspin').TouchSpin({
        min: 1,
        step: 1,
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

    // Ajax request for chained select Areas/Cities at /orders/checkout1 page
    $('select#id_anonymous_area').on('change', function() {
        var area_id = $(this).val();
        $.ajax({
            type: 'get',
            url: '/ajax/get_chained_cities/',
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

    // Ajax Landing Page Contact Form sending
    $('#landing_contact_submit').on('click', function(e) {
        e.preventDefault();
        var contact_form = $('#landing_contact_form');
        var url = contact_form.attr('action');
        var csfr_token = $('#landing_contact_form [name="csrfmiddlewaretoken"]').val();
        data = {}
        data["csrfmiddlewaretoken"] = csfr_token;
        data['contact_name'] = $('#contact_name').val();
        data['contact_email'] = $('#contact_email').val();
        data['form_content'] = $('#contact_content').val();
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function(data) {
                if (!data.error) {
                    $('#landing_modal_div p').text(data.success);
                    $('#landing_modal_div').attr('class', 'col-md-12');
                    $('#landing_contact_form')[0].reset(); // Cleans the form after succesful Ajax
                }
                $('#landing_modal_div p').text(data.error);
                $('#landing_modal_div').attr('class', 'col-md-12');
            }
        });
    });

});


