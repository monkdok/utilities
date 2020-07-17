$(document).ready(function () {
    function appendToCart(data) {
        $('#total-payments').text('(' + data.count + ')')
        $('.cart-items ul').append(data.payment)
    }

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
        let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
        $.ajax({
            url: url,
            data: {
            'organization': organization,
            'csrfmiddlewaretoken': csrf_token,
            },
            type: 'post',
            dataType: 'json',
            success: function (data) {
                if (data.exist == true)  {
                    alert('Payment is already in Cart')
                } else {
                    alert('else')
                    if(data.payment) {
                    appendToCart(data)
                    }
                }
            }
        })
    })


    let cartContainer = $('.cart-container')
    let cartItems = $('.cart-items')

    function toggleCart() {
        cartItems.toggle()
    }

    $('#cart').on('click', function(e) {
        e.preventDefault()
        toggleCart()
    })

    /*cartContainer.on('mouseover', function(e) {
        e.preventDefault()
        toggleCart()
    })

    cartContainer.on('mouseout', function(e) {
        e.preventDefault()
        toggleCart()
    })*/

    $(document).on('click', '.delete-item', function(e) {
        e.preventDefault()
        $(this).closest('li').remove()
    })
})




