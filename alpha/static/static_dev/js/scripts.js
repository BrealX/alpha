$(document).ready(function() {
    var product_page_form = $('#product_page_form');
    var navbar_form = $('#navbar_form');

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
                //console.log(data);
                console.log('OK');
                if (data.products_in_cart_total_qnty || data.products_in_cart_total_qnty == 0) {
                    $('#cart_qnty_subtotal').text('('+data.products_in_cart_total_qnty+')');
                    console.log(data.products);
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
                };
                    
            },
            error: function() {
                    console.log('some error');
            }
        });
        };


    // getting data from Product Page Form
    product_page_form.on('submit', function(e) {
        e.preventDefault();
        var qnty = $('#product_page_qnty').val();
        var submit_btn = $('#product_page_submit_btn');
        var product_id = submit_btn.data('product_id');
        var product_name = submit_btn.data('name');
        var product_price = submit_btn.data('price');
        var product_total_price = qnty*product_price;
        var product_image = submit_btn.data('image');
        console.log(product_id);
        console.log(product_name);


        cart_updating(product_id, qnty, is_delete=false);
    });

    // getting data from Main Page Form
    $('button[id^="main_page_submit_id"]').one('click', function (e) {
        button = $(this)
        e.preventDefault();
        var qnty = button.data('qnty');
        var product_id = button.data('product_id');
        var product_name = button.data('name');
        var product_price = button.data('price');
        var product_total_price = qnty*product_price;
        var product_image = button.data('image');
        //console.log(qnty, product_id, product_name);

        cart_updating(product_id, qnty, is_delete=false);
    });

    
    // function for opening dropdown menu at Navbar
    function showingMenu() {
        $('.dropdown-menu').toggleClass('hidden');
    };

    $('.dropmenu').mouseover(function() {
        showingMenu();
    });

    $('.dropmenu').mouseout(function() {
        showingMenu();
    });

    // function for opening dropdown basket menu at RightNavbar
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


    // delete item in cart
    /*function cart_cleaning() {
        $('.delete-item').on('click', function(e) {
            e.preventDefault();
            product_id = $(this).data("product_id");
            qnty = 0;
            console.log(product_id, qnty);
            cart_updating(product_id, qnty, is_delete=true);    
        });
    };

    cart_cleaning();*/

    $(document).on('click', '.delete-item', function(e) {
        e.preventDefault();
        product_id = $(this).data("product_id");
        qnty = 0;
        console.log(product_id, qnty);
        cart_updating(product_id, qnty, is_delete=true);
    });


    // function iterates for each product in basket total amount
    // and sums them in Total Basket (or Order) amount
    function calculatingTotalBasketAmount(){
        var total_price = 0
        $(".total-product-in-basket-amount").each(function(){
            //console.log($(this).text());
            total_price += parseFloat($(this).text());
        });
        //console.log(total_price);
        $('#total_price').text(total_price.toFixed(2) + ' UAH');
    };

    
    // function checks any quantity changes at Cart Page and makes 
    // changes to Cart.
    $(document).on('change', ".product-in-basket-qnty", function(){
        var current_qnty = $(this).val();
        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-in-basket-price').text()).toFixed(2);
        var total_amount = parseFloat(current_qnty*current_price).toFixed(2);
        current_tr.find('.total-product-in-basket-amount').text(total_amount);

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

    // Bootstrap Touchspin at Cart Page
    $(window).on('load', function() {
        $("input[name='quanitySniper']").TouchSpin();
    });

});


