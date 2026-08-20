from django.contrib import admin
from .models import Booking, BookingTraveler, SavedTraveler, Coupon

class BookingTravelerInline(admin.TabularInline):
    model=BookingTraveler; extra=0

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=('booking_id','traveler_name','user','package','travel_date','number_of_travelers','total_amount','status','payment_status')
    list_filter=('status','payment_status','travel_date'); search_fields=('booking_id','traveler_name','traveler_email','traveler_phone','user__username','package__name')
    inlines=[BookingTravelerInline]
    actions=['mark_confirmed','mark_cancelled','mark_completed']
    def mark_confirmed(self,request,queryset): queryset.update(status='confirmed')
    mark_confirmed.short_description='Mark selected bookings as Confirmed'
    def mark_cancelled(self,request,queryset): queryset.update(status='cancelled')
    mark_cancelled.short_description='Mark selected bookings as Cancelled'
    def mark_completed(self,request,queryset): queryset.update(status='completed')
    mark_completed.short_description='Mark selected bookings as Completed'

@admin.register(SavedTraveler)
class SavedTravelerAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','relation','user','phone','email')
    search_fields=('first_name','last_name','phone','email','user__username')

@admin.register(BookingTraveler)
class BookingTravelerAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','booking','relation','phone','email','nationality')
    search_fields=('first_name','last_name','phone','email','booking__booking_id')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display=('code','booking','discount_amount'); search_fields=('code','booking__booking_id')
