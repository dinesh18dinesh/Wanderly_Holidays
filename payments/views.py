from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from bookings.models import Booking


def _send_booking_confirmation_email(booking):
    subject = f"Booking Confirmed - {booking.booking_id}"
    message = (
        f"Hi {booking.user.first_name or booking.user.username},\n\n"
        f"Your booking for '{booking.package.name}' is confirmed.\n"
        f"Booking ID: {booking.booking_id}\n"
        f"Travel Date: {booking.travel_date}\n"
        f"Travelers: {booking.number_of_travelers}\n"
        f"Total Paid: Rs. {booking.total_amount}\n\n"
        "Thank you for choosing Wanderly. Safe travels!"
    )
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [booking.user.email], fail_silently=True)
    except Exception:
        pass


@login_required
def initiate_payment(request):
    booking_id = request.session.get('booking_id')
    if not booking_id:
        messages.error(request, 'No pending booking found.')
        return redirect('package_list')

    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    amount_paise = int(Decimal(booking.total_amount) * 100)
    context = {
        'booking': booking,
        'amount_paise': amount_paise,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'demo_mode': settings.PAYMENTS_DEMO_MODE,
    }

    if settings.PAYMENTS_DEMO_MODE:
        return render(request, 'payments/payment.html', context)

    import razorpay
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'receipt': booking.booking_id,
        'payment_capture': 1,
    })
    context['order_id'] = order['id']
    return render(request, 'payments/payment.html', context)


@transaction.atomic
def _confirm_booking(booking, payment_id=''):
    booking = Booking.objects.select_for_update().select_related('package').get(pk=booking.pk)
    if booking.status == 'confirmed' and booking.payment_status:
        return booking

    booking.payment_status = True
    booking.status = 'confirmed'
    booking.payment_id = payment_id
    booking.save(update_fields=['payment_status', 'status', 'payment_id'])
    return booking


@login_required
def payment_success(request):
    booking_id = request.session.get('booking_id')
    if not booking_id:
        messages.error(request, 'No pending booking found.')
        return redirect('package_list')

    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    try:
        booking = _confirm_booking(booking, payment_id=request.GET.get('payment_id', 'DEMO'))
    except ValueError as exc:
        messages.error(request, str(exc))
        return redirect('my_bookings')

    request.session.pop('booking_id', None)
    _send_booking_confirmation_email(booking)
    messages.success(request, f'Booking confirmed! Your booking ID is {booking.booking_id}.')
    return redirect('my_bookings')


@login_required
@require_POST
def verify_payment(request):
    booking_id = request.session.get('booking_id')
    if not booking_id:
        return JsonResponse({'ok': False, 'error': 'No pending booking.'}, status=400)

    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    payment_id = request.POST.get('razorpay_payment_id', '')
    order_id = request.POST.get('razorpay_order_id', '')
    signature = request.POST.get('razorpay_signature', '')

    try:
        import razorpay
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
        })
        _confirm_booking(booking, payment_id=payment_id)
        request.session.pop('booking_id', None)
        _send_booking_confirmation_email(booking)
        return JsonResponse({'ok': True, 'redirect': '/bookings/my-bookings/'})
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Payment verification failed.'}, status=400)


@login_required
def payment_failed(request):
    booking_id = request.session.get('booking_id')
    if booking_id:
        booking = Booking.objects.filter(booking_id=booking_id, user=request.user, status='pending').first()
        if booking:
            booking.status='cancelled'
            booking.save(update_fields=['status'])
            booking.package.available_seats += booking.number_of_travelers
            booking.package.save(update_fields=['available_seats'])
        request.session.pop('booking_id', None)
    messages.error(request, 'Payment was cancelled or failed. You can book again anytime.')
    return redirect('package_list')
