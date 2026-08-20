from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render

from bookings.models import Booking
from destinations.models import Destination, TravelPackage, Review, Enquiry


def staff_required(view_func):
    return user_passes_test(lambda u: u.is_active and u.is_staff, login_url='/accounts/login/')(view_func)


@staff_required
def dashboard(request):
    bookings = Booking.objects.select_related('user', 'package').all()
    recent_bookings = bookings[:8]

    total_revenue = bookings.filter(payment_status=True).aggregate(total=Sum('total_amount'))['total'] or 0
    avg_booking_value = (total_revenue / bookings.count()) if bookings.count() else 0
    pending_bookings = bookings.filter(status='pending').count()
    confirmed_bookings = bookings.filter(status='confirmed').count()

    context = {
        'active': 'overview',
        'total_packages': TravelPackage.objects.count(),
        'featured_packages': TravelPackage.objects.filter(is_featured=True).count(),
        'total_destinations': Destination.objects.count(),
        'total_bookings': bookings.count(),
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'total_users': User.objects.filter(is_staff=False).count(),
        'staff_users': User.objects.filter(is_staff=True).count(),
        'total_reviews': Review.objects.count(),
        'pending_reviews': Review.objects.filter(is_approved=False).count(),
        'total_enquiries': Enquiry.objects.count(),
        'pending_enquiries': Enquiry.objects.exclude(status='closed').count(),
        'total_revenue': total_revenue,
        'avg_booking_value': avg_booking_value,
        'recent_bookings': recent_bookings,
        'top_packages': TravelPackage.objects.order_by('-is_featured', '-created_at')[:5],
    }
    return render(request, 'admin_dashboard/dashboard.html', context)
