from .models import PaymentInCart


def getting_cart_info(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    payments = PaymentInCart.objects.filter(session_key=session_key)
    total_payments = payments.count()
    return {
        'total_payments': total_payments,
        'payments_in_cart': payments,
    }