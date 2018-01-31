$(document).ready(function() {
    var form = $('#form-buying-product');
    console.log(form);

    function basketUpdating(product_id, nmb, is_delete){
        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;
        var csfr_token = $('#form-buying-product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csfr_token;

        if (is_delete){
            data["is_delete"] = true;
        }

        var url = form.attr("action");
        console.log(data)
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function(data) {
                console.log('OK');
                console.log(data.products_total_nmb)
                if (data.products_total_nmb || data.products_total_nmb == 0) {
                    $('#basket_total_nmb').text("("+data.products_total_nmb+")");
                    console.log(data.products);
                    $('.basket-items ul').html('');
                    $.each(data.products, function(k, v) {
                        $('.basket-items ul').append('<li>' + v.name + ', ' + v.nmb + ' шт. ' + 'по ' + v.price_per_item + ' грн   ' +
                        '<a class="delete-item" href="" data-product_id="'+v.id+'">x</a>' +
                        '</li>');
                    })
                }
            },
            error: function() {
                console.log('error');
            }
        })
    }

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
        console.log(name);

        basketUpdating(product_id, nmb, is_delete=false);

    })

    function showingBasket() {
        $('.basket-items').toggleClass('hidden');
    };

    $('.basket-container').mouseover(function() {
        showingBasket();
    });

    $('.basket-container').mouseout(function() {
        showingBasket();
    });

    $(document).on('click', '.delete-item', function(e) {
        e.preventDefault();
        product_id = $(this).data("product_id");
        nmb = 0;
        basketUpdating(product_id, nmb, is_delete=true);
    });

    function calculatingBasketAmount(){
        var total_order_amount = 0;
        $('.total-product-in-basket-amount').each(function(){
            total_order_amount += parseFloat($(this).text());
        });
        console.log(total_order_amount);
        $('#total_order_amount').text(total_order_amount.toFixed(2));
    };

    $(document).on('change', ".product-in-basket-nmb", function(){
        var current_nmb = $(this).val();
        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        var total_amount = parseFloat(current_nmb*current_price).toFixed(2);
        current_tr.find('.total-product-in-basket-amount').text(total_amount);

        calculatingBasketAmount();
    });

    calculatingBasketAmount();

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



