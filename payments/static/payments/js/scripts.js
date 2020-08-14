$(document).ready(function () {
    let cartContainer = $('.cart-container')
    let cartItems = $('.cart-items')


    function appendToCart(data) {
        $('#total-payments').text(" " + data.count)
        $('#cart-snippet').append(data.payment)
    }

    function appendToHtml(data) {
        $('.icon-on-button').html(data)
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
        $('.cart-is-empty').hide()
    })



    /*$(document).mouseup(function (e) {
            if(!cartItems.is(e.target) &&
            cartItems.has(e.target).length === 0) {
                cartItems.hide()
            }
        })*/


// Delete cart item
    $(document).on('click', '.delete-item', function(e) {
        e.preventDefault()
        let paymentInCartId = $(this).attr('data-payments-in-cart-pk')
        let url = $(this).attr('href')
        cartUpdate(paymentInCartId, url, is_delete=true)
        $(this).closest('li').remove()
        $('.checkout-button').hide()
        $('.cart-is-empty').show()
        cartItems.show()
    })

    function calculation() {
        let totalPrice = 0
        $('.price').each(function(){
            totalPrice += parseFloat($(this).text())
        })
        return totalPrice.toFixed(2)
    }
    $('#total-price').text(calculation())


//Getting Icon ID
    $('.dropdown-icon').on('click', function() {
        let pk = $(this).attr('data-icon-pk')
        let input = $('input#icon-pk')
        input.val(pk)
        let csrf_token = jQuery("[name=csrfmiddlewaretoken]").val()
        let url = $(this).attr('data-url')
        $.ajax({
            url: url,
            // data: form.serialize(),
            data: {pk: pk},
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                if (data) {
                    $('.icon-on-button').html(data.html)
                }
                else {
                    alert("All fields must have a valid value.")
                }
            }
        })
    })


////Update Service
//    let unitsOnButton = $('.unit-on-button').text()
//    let iconOnButton = $('.icon-on-button img').data('src')
//    $('#measurement_units').val(unitsOnButton)
//    $('#icon').val(iconOnButton)

//Getting Units
    $('.dropdown-unit').on('click', function() {
        let unit = $(this).text()
        $('.unit-on-button').text(unit)
        $('#measurement_units').val(unit)

    })

//Calculator
    $(document).on('input', '#current_counter_value, #previous_counter_value', function() {
        let currentValue = parseInt($('#current_counter_value').val())
        let previousValue = parseInt($('#previous_counter_value').val())
        let tariff = $('#tariff').val()
        let difference = $('#difference')
        let calculationResult = $('#result')

        if (isNaN(previousValue)) {
            previousValue = 0
        }
        let differenceCalc = currentValue - previousValue
        let price = differenceCalc * tariff
        if (currentValue > previousValue) {
            difference.text(differenceCalc)
            calculationResult.text(price.toFixed(2))
            $('.difference-result').css('display', 'flex')
            $('.units, .currency').show()
        } else {
            calculationResult.text('')
            difference.text('')
            $('.difference-result').css('display', 'none')
            $('.units, .currency').hide()
        }
    })



// Toggle cart
//    $('#cart').on('click', function(e) {
//        e.preventDefault()
//        toggleCart()
//    })

function getParent(id) {
    if ($elem.parents('.left').length != 0) {
    //someone has this class
}
   return event.target.parentNode;
}



//$(document).click(function(e){
////    let el = $('.' + e.target.className)
////    console.log(el)
//    console.log($(e.target).parents())
//
//    if ($(e.target).parents('.cart-items').length) {
//        console.log('yeah')
//        }
//
//})

$(document).click(function(e){
//     e.stopPropagation()
        if ( ($(e.target).parents('#cart').length) || (e.target.id == 'cart')) {
        e.preventDefault()
//        toggleCart()
          cartItems.toggle()
        } else if (($(e.target).parents('.cart-items').length ) || ($(e.target).attr('class') == 'cart-items')) {
            cartItems.show()
        } else {
            cartItems.hide()
        }
    })

$(document).click(function(e) {
    if (($(e.target).parents('.delete-item').length) || ($(e.target).attr('class') == 'delete-item')) {
        cartItems.show()
    }
})

//    if ($(this) != cartItems) {
//        cartItems.hide()
//    }

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