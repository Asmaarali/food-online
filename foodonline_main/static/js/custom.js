$(document).ready(function () {
    // Add to cart 
    $('.add_to_cart').on('click', function (e) {
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        data = {
            food_id: food_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function (response) {
                // console.log(response)
                // console.log(response.cart_counter['cart_count']) //cart_count is coming from function in dict type 
                if(response.status=="login_required"){
                    // console.log(response)
                    Swal.fire(response.message, '','info').then(function(){
                        window.location = '/login'
                    })
                }else if(response.status=="failed"){
                    Swal.fire(response.message, '','error')
                }
                else{
                $('#cart_counter').html(response.cart_counter['cart_count']);
                $('#qty-' + food_id).html(response.qty);               //locate the first tag  
                
                // cart amount function calculation
                if(window.location.pathname === '/marketplace/cart/'){
                    cartamountpushhtml(response.cart_amount['subtotal'],response.cart_amount['tax'],response.cart_amount['grand_total'])
                
                }

                }
            }
        })

    })


    // Decrease to cart 
    $('.decrease_cart').on('click', function (e) {
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id'); //for cart page removing item if 0

        data = {
            food_id: food_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function (response) {
                // console.log(response)
                // console.log(response.cart_counter['cart_count']) //cart_count is coming from function in dict type 
                if(response.status=="login_required"){
                    // console.log(response)
                    Swal.fire(response.message, '','info').then(function(){
                        window.location = '/login'
                    })
                }else if(response.status=="failed"){
                    Swal.fire(response.message, '','error')
                }
                else{
                $('#cart_counter').html(response.cart_counter['cart_count']);
                $('#qty-' + food_id).html(response.qty);

                //for cart page removing item if 0
                // put in if condition because it should only work in cart page
                // alert(cart_id)
                // console.log('Current pathname:', window.location.pathname);
                if(window.location.pathname === '/marketplace/cart/'){
                    removecartItem(response.qty,cart_id); 
                    checkCartItemsExists();    
                    
                    // #total grandtotal 
                    cartamountpushhtml(response.cart_amount['subtotal'],response.cart_amount['tax'],response.cart_amount['grand_total'])
                    
                    
                }

                }

            }
        })

    })

    // place the cart_item on load file in vendordetail.html
    $('.item_qty').each(function () {
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        // alert("id "+the_id+", quantity"+qty)
        $('#' + the_id).html(qty) //it will match first matching tag
    })


    // check_emailaddress_exists
    $('#id_email').on('keyup', function (e) {
        e.preventDefault();

        var email = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/check_user_exists/',
            data: { email: email },
            success: function (data) {
                // alert(JSON.stringify(data))

                if (data.status == 1) {
                    $('#messagejson').text(data.message);
                    // alert(JSON.stringify(data))
                }
                else {
                    $('#messagejson').text('');
                    // alert(JSON.stringify(data))
                }
            }
        })
    })

    // check_username_exists
    $('#id_username').on('keyup', function (e) {
        e.preventDefault();

        var username = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/check_username_exists/',
            data: { username: username },
            success: function (data) {
                // alert(JSON.stringify(data))

                if (data.status == 1) {
                    $('#usermessagejson').text(data.message);
                    // alert(JSON.stringify(data))
                }
                else {
                    $('#usermessagejson').text('');
                    // alert(JSON.stringify(data))
                }
            }
        })
    })


    // # cart page delete cart
    $('.delete_cart').on('click', function (e) {
        e.preventDefault();

        url = $(this).attr('data-url');
        cart_id = $(this).attr('data-id');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                // console.log(response)
                // console.log(response.cart_counter['cart_count']) //cart_count is coming from function in dict type 
                if(response.status=="failed"){
                    Swal.fire(response.message, '','error')
                }
                else{
                $('#cart_counter').html(response.cart_counter['cart_count']);
                Swal.fire(response.status,response.message,'success') 
                removecartItem(0,cart_id) 
                checkCartItemsExists()
                
                // total grand total delete update 
                if(window.location.pathname === '/marketplace/cart/'){
                    cartamountpushhtml(response.cart_amount['subtotal'],response.cart_amount['tax'],response.cart_amount['grand_total'])
                
                }

                }
            }
        })

    })
    // # remove cart element without reloading after deleting
    function removecartItem(cartItemqty , cart_id){
        if (cartItemqty <= 0){
        document.getElementById("cart-item-"+cart_id).remove()
        }
    }

    // # removing display none for showing text(cart is empty) without reloading page
    function checkCartItemsExists(){
        cart = document.getElementById("cart_counter").innerHTML //read the cart counter number
        if (cart == 0){
            document.getElementById("empty-cart").style.display = "block";
        }
    }

    function cartamountpushhtml(subtotal , tax , grand_total){
        $('#subtotal').html(subtotal)
        $('#tax').html(tax)
        $('#total').html(grand_total)
    }

});

