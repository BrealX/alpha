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

    // Changes product in cart quantity when user makes changes at Checkout Page with touchspin plugin
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

    // Delete items from miniCart
    $('div.minicart-button').on('click', 'a.delete-item', function(e) {
        e.preventDefault();
        var cart_changes = {};
        product_id = $(this).data("product_id");
        qnty = 0;
        cart_changes[product_id] = {qnty: qnty, is_delete: true};
    
        cart_updating(cart_changes);
	});

    // Delete items from Checkout Page
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

    // Add to Wishlist Click Event
    $('.add-fav').click(function (e) {
        e.preventDefault();
        $(this).addClass("active"); // ADD TO WISH LIST BUTTON 
        $(this).attr('data-original-title', 'Понравилось');// Change Tooltip text
    });

    // Bootstrap Touchspin at Cart Page Initializer
    $('.cart-touchspin').TouchSpin({
        min: 1,
        step: 1,
    });

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
                if (!data.profile_delivery_city) {
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
                    $('.profile-firstname, .profile_phone').html("");
                    $('.profile-firstname').text("Вы не указали имя");
                    $('.profile-phone').text("Вы не указали контактный номер телефона");
                };
            }
        });
    });

    // My Profile Reviews Page review delete button
    $('#deletefeedbackModal .btn-delete').on('click', function(e) {
        e.preventDefault();
        var form = $('#review_delete_form');
        var url = form.attr('action');
        var csfr_token = $('#review_delete_form [name="csrfmiddlewaretoken"]').val();
        var feedback_id = $('#delete_input').val();
        var redirect_url = $('#go_back_form').attr('action');
        data = {}
        data["csrfmiddlewaretoken"] = csfr_token;
        data["feedback_id"] = feedback_id;
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function(data) {
                window.location.href = redirect_url;
            }
        });
    });

    // Modal window on account deletion (delete confirmation & delete process)
    $('div#deleteModalCenter').on('show.bs.modal', function(e) {
        $(this).find('.btn-delete').attr('href', $(e.relatedTarget).data('href'));
    });
    $('div#deleteModalCenter').on('click', '.btn-delete', function(e) {
        e.preventDefault();
        var account_delete_form = $('#my_account_delete_form');
        var url = account_delete_form.attr('action');
        var go_home_form = $('#go_home_form');
        var redirect_url = go_home_form.attr('action');
        var csfr_token = $('#my_account_delete_form [name="csrfmiddlewaretoken"]').val();
        data = {};
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
                    $('#landing_contact_form')[0].reset(); // Cleans the form after successful Ajax
                }
                $('#landing_modal_div p').text(data.error);
                $('#landing_modal_div').attr('class', 'col-md-12');
            }
        });
    });

    // Checkout2 Page order confirmation
    $('#order_confirm_button').on('click', function(e) {
        e.preventDefault();
        var order_confirm_button = $(this);
        var url = order_confirm_button.attr("href");
        var data = {};
        data['order_id'] = $('#checkout2_page_order_id').attr('value');

        $.ajax({
            url: url,
            type: 'GET',
            data: data,
            cache: true,
            success: function(data) {
                if (data.order_id) {
                    $("#order_info_modal").modal('show');
                    var order_id = data.order_id;
                    var order_overall = data.order_overall;
                    var order_customer_email = data.order_customer_email;
                    var order_customer_name = data.order_customer_name;
                    var notification_url = $('#order_notification_form').attr('action');
                    var data = {};
                    data['order_id'] = order_id;
                    data['order_overall'] = order_overall;
                    data['order_customer_email'] = order_customer_email;
                    data['order_customer_name'] = order_customer_name;

                    $.ajax({
                        url: notification_url,
                        type: 'GET',
                        data: data,
                        cache: true,
                    });
                };
            }
        });
    });

    // Redirects to Home Page when Order Info Close Button clicked
    $('#order_info_modal_close').on('click', function(e) {
        e.preventDefault();
        window.location.href = '/';
    });

    // Shows full feedback text at modal window when 'Read more' button is clicked at Landing Page
    $('#feedbackModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var username = button.data('username');
        var feedback_text = button.data('feedback_text');
        var modal = $(this);
        modal.find('.modal-title').text('Отзыв от пользователя ' + username);
        modal.find('.modal-body .review-form-container').text(feedback_text);
    });

});