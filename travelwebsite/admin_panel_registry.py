"""
Declarative registry that drives the custom-styled admin CRUD panel.

Each entry describes one management section: which model backs it, which
columns show on the list page, which fields appear on the add/edit form,
and which fields are searchable. The generic views + templates in
`admin_panel_views.py` read this config so every section gets full,
consistently-styled Create / Read / Update / Delete without a bespoke
template per model.

`list_fields` items are tuples: (attribute, label, kind)
  kind is one of: text, date, datetime, currency, badge, boolean, image, email, count
"badge" fields use BADGE_MAP to colour the pill based on the raw value.
"""
from bookings.models import Booking
from destinations.models import (
    BlogPost, Coupon, Destination, Enquiry, NewsletterSubscriber,
    Review, Testimonial, TravelPackage,
)

# value -> css modifier class, used for any "badge" kind list field
BADGE_MAP = {
    'pending': 'orange', 'new': 'orange',
    'confirmed': 'green', 'contacted': 'blue', 'converted': 'green', 'active': 'green', 'yes': 'green', True: 'green',
    'cancelled': 'red', 'closed': 'gray', 'inactive': 'gray', 'no': 'gray', False: 'gray',
    'completed': 'purple',
}


SECTIONS = {
    'bookings': dict(
        model=Booking,
        title='Bookings',
        singular='Booking',
        icon='fa-regular fa-calendar-check',
        order_by='-created_at',
        search_fields=['booking_id', 'traveler_name', 'traveler_phone', 'traveler_email', 'user__username', 'package__name'],
        list_fields=[
            ('booking_id', 'Booking ID', 'text'),
            ('traveler_name_display', 'Traveler', 'text'),
            ('package', 'Package', 'text'),
            ('travel_date', 'Travel Date', 'date'),
            ('number_of_travelers', 'Pax', 'count'),
            ('total_amount', 'Amount', 'currency'),
            ('status', 'Status', 'badge'),
            ('payment_status', 'Paid', 'boolean'),
        ],
        form_fields=[
            'user', 'package', 'travel_date', 'number_of_travelers', 'traveler_name',
            'traveler_phone', 'traveler_email', 'total_amount', 'discount_amount',
            'coupon_code', 'special_requests', 'status', 'payment_status', 'payment_id',
        ],
    ),
    'packages': dict(
        model=TravelPackage,
        title='Packages',
        singular='Package',
        icon='fa-solid fa-cube',
        order_by='-is_featured,-created_at',
        search_fields=['name', 'destination__name', 'destination__city'],
        list_fields=[
            ('image_src', 'Image', 'image'),
            ('name', 'Package', 'text'),
            ('destination', 'Destination', 'text'),
            ('package_type', 'Type', 'badge'),
            ('duration_days', 'Days', 'count'),
            ('price', 'Price', 'currency'),
            ('available_seats', 'Seats', 'count'),
            ('is_featured', 'Featured', 'boolean'),
        ],
        form_fields=[
            'name', 'destination', 'description', 'duration_days', 'price', 'discount_price',
            'package_type', 'tour_type', 'group_size', 'languages', 'highlights', 'inclusions',
            'exclusions', 'itinerary', 'main_image', 'image_url', 'gallery_urls', 'travel_guide',
            'faqs', 'insurance_included', 'is_featured', 'available_seats',
        ],
    ),
    'destinations': dict(
        model=Destination,
        title='Destinations',
        singular='Destination',
        icon='fa-solid fa-location-dot',
        order_by='-is_featured,-created_at',
        search_fields=['name', 'city', 'country'],
        list_fields=[
            ('image_src', 'Image', 'image'),
            ('name', 'Name', 'text'),
            ('city', 'City', 'text'),
            ('country', 'Country', 'text'),
            ('best_time_to_visit', 'Best Time', 'text'),
            ('is_featured', 'Featured', 'boolean'),
        ],
        form_fields=[
            'name', 'city', 'country', 'description', 'image', 'image_url', 'gallery_urls',
            'latitude', 'longitude', 'best_time_to_visit', 'is_featured', 'highlights',
            'travel_guide', 'things_to_do',
        ],
    ),
    'reviews': dict(
        model=Review,
        title='Reviews & Ratings',
        singular='Review',
        icon='fa-regular fa-star',
        order_by='-created_at',
        search_fields=['user__username', 'package__name', 'comment'],
        list_fields=[
            ('user', 'User', 'text'),
            ('package', 'Package', 'text'),
            ('rating', 'Rating', 'stars'),
            ('comment', 'Comment', 'truncate'),
            ('is_approved', 'Approved', 'boolean'),
            ('created_at', 'Date', 'date'),
        ],
        form_fields=['user', 'package', 'rating', 'comment', 'is_approved'],
    ),
    'enquiries': dict(
        model=Enquiry,
        title='Enquiries',
        singular='Enquiry',
        icon='fa-regular fa-circle-question',
        order_by='-created_at',
        search_fields=['name', 'email', 'phone', 'destination', 'city'],
        list_fields=[
            ('name', 'Name', 'text'),
            ('destination', 'Destination', 'text'),
            ('email', 'Email', 'email'),
            ('phone', 'Phone', 'text'),
            ('travel_date', 'Travel Date', 'date'),
            ('vacation_type', 'Type', 'badge'),
            ('status', 'Status', 'badge'),
        ],
        form_fields=[
            'name', 'city', 'email', 'phone', 'whatsapp', 'destination', 'travel_date',
            'travelers', 'vacation_type', 'message', 'status',
        ],
    ),
    'coupons': dict(
        model=Coupon,
        title='Coupons',
        singular='Coupon',
        icon='fa-solid fa-ticket',
        order_by='-valid_to',
        search_fields=['code'],
        list_fields=[
            ('code', 'Code', 'text'),
            ('discount_percent', 'Discount', 'percent'),
            ('valid_from', 'Valid From', 'date'),
            ('valid_to', 'Valid To', 'date'),
            ('is_active', 'Active', 'boolean'),
        ],
        form_fields=['code', 'discount_percent', 'valid_from', 'valid_to', 'is_active'],
    ),
    'newsletter': dict(
        model=NewsletterSubscriber,
        title='Newsletter Subscribers',
        singular='Subscriber',
        icon='fa-regular fa-envelope',
        order_by='-subscribed_at',
        search_fields=['email'],
        list_fields=[
            ('email', 'Email', 'email'),
            ('is_active', 'Active', 'boolean'),
            ('subscribed_at', 'Subscribed', 'date'),
        ],
        form_fields=['email', 'is_active'],
    ),
    'testimonials': dict(
        model=Testimonial,
        title='Testimonials',
        singular='Testimonial',
        icon='fa-solid fa-quote-left',
        order_by='-is_featured,-created_at',
        search_fields=['name', 'location', 'message'],
        list_fields=[
            ('name', 'Name', 'text'),
            ('location', 'Location', 'text'),
            ('rating', 'Rating', 'stars'),
            ('message', 'Message', 'truncate'),
            ('is_featured', 'Featured', 'boolean'),
        ],
        form_fields=['name', 'location', 'rating', 'message', 'is_featured'],
    ),
    'blogposts': dict(
        model=BlogPost,
        title='Blog Posts',
        singular='Blog Post',
        icon='fa-regular fa-newspaper',
        order_by='-published_at',
        search_fields=['title', 'excerpt'],
        list_fields=[
            ('blog_image_url', 'Image', 'image'),
            ('title', 'Title', 'text'),
            ('is_published', 'Published', 'boolean'),
            ('published_at', 'Date', 'date'),
        ],
        form_fields=['title', 'excerpt', 'content', 'image', 'is_published', 'published_at'],
    ),
}
