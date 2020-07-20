$(document).ready(function () {
    let cartContainer = $('.cart-container')
    let cartItems = $('.cart-items')


    function appendToCart(data) {
        $('#total-payments').text('(' + data.count + ')')
        $('#cart-snippet').append(data.payment)
    }


    function toggleCart() {
        cartItems.toggle()
    }


    function cartUpdate(pk, url, is_delete=false) {
        let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
        $.ajax({
//            url: $('#add-to-cart-form').attr('action'),
            url: url,
            data: {
            'is_delete': is_delete,
            'pk': pk,
            'csrfmiddlewaretoken': csrf_token,
            },
            type: 'post',
            dataType: 'json',
            success: function (data) {
                if (data.exist == true)  {
                    alert('Payment is already in Cart')
                    console.log('data.exist == true')
                } else {
                    if(data.payment || data.deleted) {
                    appendToCart(data)
                    }
                }
            }
        })
    }

// Add item to cart
    $('form#add-to-cart-form').on('submit', function(e) {
        e.preventDefault()
        let organization = $('#form-organization').val()
        let paymentPeriod = $('#organization').val()
        let date = $('#organization').val()
        let tariff = $('#organization').val()
        let previousValue = $('#form-previous_value').val()
        let currentValue = $('#form-current_value').val()
        let difference = $('#form-difference').val()
        let units = $('#form-units').val()
        let price = $('#form-price').val()
        let url = $(this).attr('action')
        cartUpdate('0', url)
    })


// Toggle cart
    $('#cart').on('click', function(e) {
        e.preventDefault()
        toggleCart()
    })


// Delete cart item
    $(document).on('click', '.delete-item', function(e) {
        e.preventDefault()
        console.log('clicked')
        let paymentInCartId = $(this).attr('data-payments-in-cart-pk')
        let url = $(this).attr('href')
        cartUpdate(paymentInCartId, url, is_delete=true)
        $(this).closest('li').remove()
    })
})





    /*let addButton = $('#btn-add-to-cart')
    addButton.on('click', function(e) {
        e.preventDefault()
        let organization = addButton.attr('data-organization')
        let paymentPeriod = addButton.attr('data-payment-period')
        let date = addButton.attr('data-date')
        let tariff = addButton.attr('data-tariff')
        let previousValue = addButton.attr('data-previous-value')
        let currentValue = addButton.attr('data-current-value')
        let difference = addButton.attr('data-difference')
        let units = addButton.attr('data-units')
        let price = addButton.attr('data-price')

*//*
        $('.cart-container a').text('Cart(1)')
*//*
        let url = addButton.attr('data-url')
         let pk = addButton.attr('data-pk')*/