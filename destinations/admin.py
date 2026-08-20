from django.contrib import admin
from .models import (
    BlogPost, Coupon, Destination, Enquiry, ItineraryDay, NewsletterSubscriber,
    Review, Testimonial, TravelPackage, Wishlist
)


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'is_featured', 'created_at')
    list_filter = ('country', 'is_featured')
    search_fields = ('name', 'city', 'country', 'description')
    fieldsets = (
        ('Destination Basics', {'fields': ('name', 'slug', 'city', 'country', 'description', 'image', 'image_url', 'gallery_urls', 'is_featured')}),
        ('Planning Information', {'fields': ('best_time_to_visit', 'highlights', 'things_to_do', 'travel_guide', 'latitude', 'longitude')}),
    )
    prepopulated_fields = {'slug': ('name',)}


class ItineraryDayInline(admin.TabularInline):
    model = ItineraryDay
    extra = 1
    ordering = ('day_number',)
    fields = ('day_number', 'title', 'description', 'activities', 'meals', 'overnight_stay')


@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'package_type', 'tour_type', 'price', 'discount_price', 'available_seats', 'is_featured')
    list_filter = ('package_type', 'tour_type', 'is_featured', 'destination')
    search_fields = ('name', 'destination__name', 'destination__city')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ItineraryDayInline]
    fieldsets = (
        ('Basic Information', {'fields': ('name', 'slug', 'destination', 'description', 'main_image', 'image_url', 'gallery_urls')}),
        ('Traveler Experience', {'fields': ('travel_guide', 'faqs', 'insurance_included')}),
        ('Tour Details', {'fields': ('package_type', 'tour_type', 'duration_days', 'group_size', 'languages', 'highlights')}),
        ('Pricing & Availability', {'fields': ('price', 'discount_price', 'available_seats', 'is_featured')}),
        (
            'Itinerary (legacy text, optional)',
            {
                'fields': ('itinerary', 'inclusions', 'exclusions'),
                'description': (
                    'The day-by-day itinerary shown on the package page is edited below in '
                    '"Itinerary days". This text field is only used as a fallback if no '
                    'itinerary days have been added yet.'
                ),
            },
        ),
    )


@admin.register(ItineraryDay)
class ItineraryDayAdmin(admin.ModelAdmin):
    list_display = ('package', 'day_number', 'title', 'meals')
    list_filter = ('meals',)
    search_fields = ('package__name', 'title', 'description')
    ordering = ('package', 'day_number')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating')
    search_fields = ('user__username', 'package__name', 'comment')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'added_at')
    search_fields = ('user__username', 'package__name')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code',)


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'phone', 'travelers', 'vacation_type', 'status', 'created_at')
    list_filter = ('status', 'vacation_type')
    search_fields = ('name', 'email', 'phone', 'destination')
    list_editable = ('status',)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active',)
    search_fields = ('email',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'is_featured', 'created_at')
    list_filter = ('rating', 'is_featured')
    search_fields = ('name', 'location', 'message')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
