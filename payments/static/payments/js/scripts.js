$(document).ready(function () {
    let addButton = $('#btn-add-to-cart')
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
        $('.cart-items ul').append('<li>' + '<h4>' + organization + '</h4>' + 'price: ' + price + ' ' + '<a href="" class="delete-item">X</a>' + '</li>')
/*
        $('.cart-container a').text('Cart(1)')
*/
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
});