import random
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from destinations.models import TravelPackage


class Booking(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('confirmed','Confirmed'),('cancelled','Cancelled'),('completed','Completed')]
    booking_id = models.CharField(max_length=30, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE, related_name='bookings')
    travel_date = models.DateField()
    number_of_travelers = models.PositiveIntegerField(default=1)
    traveler_name = models.CharField(max_length=120, blank=True)
    traveler_phone = models.CharField(max_length=30, blank=False)
    traveler_email = models.EmailField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon_code = models.CharField(max_length=30, blank=True)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = f"TRV{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100,999)}"
        super().save(*args, **kwargs)

    @property
    def gross_amount(self):
        return self.package.effective_price * self.number_of_travelers

    def __str__(self):
        return self.booking_id


class BookingTraveler(models.Model):
    GENDER_CHOICES = [('male','Male'),('female','Female'),('other','Other')]
    RELATION_CHOICES = [('self','Self'),('spouse','Spouse'),('child','Child'),('parent','Parent'),('sibling','Sibling'),('friend','Friend'),('other','Other')]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='traveler_details')
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80, blank=True)
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES, default='friend')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    nationality = models.CharField(max_length=80, blank=True, default='Indian')
    phone = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=True)
    passport_number = models.CharField(max_length=40, blank=True)
    id_number = models.CharField(max_length=60, blank=True)
    special_needs = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class SavedTraveler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_travelers')
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80, blank=True)
    relation = models.CharField(max_length=20, choices=BookingTraveler.RELATION_CHOICES, default='friend')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=BookingTraveler.GENDER_CHOICES, blank=True)
    nationality = models.CharField(max_length=80, blank=True, default='Indian')
    phone = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=True)
    passport_number = models.CharField(max_length=40, blank=True)
    id_number = models.CharField(max_length=60, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class Coupon(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='coupon_used')
    code = models.CharField(max_length=30)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self): return f"{self.code} on {self.booking.booking_id}"
