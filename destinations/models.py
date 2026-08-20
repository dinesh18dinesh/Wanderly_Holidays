from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class Destination(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='Optional remote image URL used when no uploaded image is available.')
    gallery_urls = models.TextField(blank=True, help_text='Optional image URLs, one per line, for the destination gallery.')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    highlights = models.TextField(blank=True, help_text='One destination highlight per line')
    travel_guide = models.TextField(blank=True, help_text='Practical travel guide information')
    things_to_do = models.TextField(blank=True, help_text='One experience/activity per line')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.city}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('destination_detail', kwargs={'slug': self.slug})

    @property
    def image_src(self):
        if self.image:
            return self.image.url
        return self.image_url

    @property
    def gallery_list(self):
        return [u.strip() for u in self.gallery_urls.splitlines() if u.strip()]

    @property
    def gallery_display_list(self):
        # Only images assigned to this destination are displayed.
        images = []
        if self.image_src:
            images.append(self.image_src)
        images.extend(self.gallery_list)
        return list(dict.fromkeys(images))[:5]

    @property
    def highlights_list(self):
        return [h.strip() for h in self.highlights.splitlines() if h.strip()]

    @property
    def things_to_do_list(self):
        return [x.strip() for x in self.things_to_do.splitlines() if x.strip()]

    @property
    def map_embed_url(self):
        """OpenStreetMap embed URL centred on this destination. No API key needed."""
        if self.latitude is None or self.longitude is None:
            return ''
        lat, lon = float(self.latitude), float(self.longitude)
        delta = 0.08
        bbox = f"{lon - delta},{lat - delta},{lon + delta},{lat + delta}"
        return f"https://www.openstreetmap.org/export/embed.html?bbox={bbox}&layer=mapnik&marker={lat},{lon}"

    @property
    def map_link_url(self):
        """Link to the full OpenStreetMap view (used for the 'View larger map' link)."""
        if self.latitude is None or self.longitude is None:
            return ''
        return f"https://www.openstreetmap.org/?mlat={self.latitude}&mlon={self.longitude}#map=11/{self.latitude}/{self.longitude}"

    def __str__(self):
        return self.name


class TravelPackage(models.Model):
    PACKAGE_TYPES = [
        ('adventure', 'Adventure'),
        ('beach', 'Beach'),
        ('cultural', 'Cultural'),
        ('wildlife', 'Wildlife'),
        ('pilgrimage', 'Pilgrimage'),
        ('honeymoon', 'Honeymoon'),
        ('family', 'Family'),
        ('educational', 'Educational'),
        ('corporate', 'Corporate'),
        ('luxury', 'Luxury'),
    ]
    TOUR_TYPES = [
        ('daily', 'Daily Tour'),
        ('private', 'Private Tour'),
        ('group', 'Group Departure'),
        ('custom', 'Custom Tour'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    description = models.TextField()
    duration_days = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES, default='cultural')
    tour_type = models.CharField(max_length=20, choices=TOUR_TYPES, default='daily')
    group_size = models.CharField(max_length=50, default='Unlimited')
    languages = models.CharField(max_length=200, default='English')
    highlights = models.TextField(blank=True, help_text="One highlight per line")
    inclusions = models.TextField(help_text="Comma-separated list of inclusions", blank=True)
    exclusions = models.TextField(help_text="Comma-separated list of exclusions", blank=True)
    itinerary = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='packages/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='Optional remote cover image URL used when no uploaded image is available.')
    gallery_urls = models.TextField(blank=True, help_text='Optional image URLs, one per line, for the package gallery.')
    travel_guide = models.TextField(blank=True, help_text='Package-specific travel guide')
    faqs = models.TextField(blank=True, help_text='One FAQ per line. Format: Question | Answer')
    insurance_included = models.BooleanField(default=True, help_text='Show travel insurance as included in this package.')
    is_featured = models.BooleanField(default=False)
    available_seats = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('package_detail', kwargs={'slug': self.slug})

    @property
    def image_src(self):
        if self.main_image:
            return self.main_image.url
        return self.image_url

    @property
    def gallery_list(self):
        return [u.strip() for u in self.gallery_urls.splitlines() if u.strip()]

    @property
    def gallery_display_list(self):
        images = []
        if self.image_src:
            images.append(self.image_src)
        images.extend(self.gallery_list)
        # Do not inject generic travel images here. The seed catalogue
        # supplies five destination-specific images for every package.
        return images[:5]

    @property
    def faq_list(self):
        items = []
        for line in self.faqs.splitlines():
            if '|' in line:
                question, answer = line.split('|', 1)
                items.append((question.strip(), answer.strip()))
        return items

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def discount_percent(self):
        if self.discount_price and self.price and self.discount_price < self.price:
            return round((1 - (self.discount_price / self.price)) * 100)
        return 0

    @property
    def inclusions_list(self):
        return [i.strip() for i in self.inclusions.split(',') if i.strip()]

    @property
    def exclusions_list(self):
        return [e.strip() for e in self.exclusions.split(',') if e.strip()]

    @property
    def highlights_list(self):
        return [h.strip() for h in self.highlights.splitlines() if h.strip()]

    @property
    def average_rating(self):
        return self.reviews.filter(is_approved=True).aggregate(avg=models.Avg('rating'))['avg'] or 0

    @property
    def itinerary_days_list(self):
        """Structured, per-package itinerary days managed in Admin.

        Falls back to the legacy plain-text `itinerary` field (one line per
        day, no real description) only if no structured days have been
        added yet for this package, so nothing breaks while packages are
        migrated over.
        """
        days = list(self.itinerary_days.all())
        if days:
            return days
        fallback = []
        for i, line in enumerate(self.itinerary.splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            fallback.append(ItineraryDay(package=self, day_number=i, title=line, description=''))
        return fallback

    def __str__(self):
        return self.name


class ItineraryDay(models.Model):
    MEAL_CHOICES = [
        ('', 'Not specified'),
        ('B', 'Breakfast'),
        ('BL', 'Breakfast & Lunch'),
        ('BD', 'Breakfast & Dinner'),
        ('BLD', 'Breakfast, Lunch & Dinner'),
        ('none', 'No meals included'),
    ]

    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE, related_name='itinerary_days')
    day_number = models.PositiveIntegerField(help_text='Day 1, Day 2, etc.')
    title = models.CharField(max_length=200, help_text="Short headline for the day, e.g. 'Arrival in Goa & beach relaxation'")
    description = models.TextField(
        blank=True,
        help_text='What actually happens this day: sights, transfers, meals, free time. This is specific to this package.'
    )
    activities = models.TextField(
        blank=True,
        help_text='One activity/stop per line for this day, e.g. "Old Goa heritage walk" (optional).'
    )
    meals = models.CharField(max_length=10, choices=MEAL_CHOICES, blank=True, default='')
    overnight_stay = models.CharField(max_length=150, blank=True, help_text='Optional: city/hotel where the traveler stays overnight, e.g. "Overnight in Baga, Goa"')

    class Meta:
        ordering = ['package', 'day_number']
        constraints = [
            models.UniqueConstraint(fields=['package', 'day_number'], name='unique_package_day_number')
        ]

    @property
    def activities_list(self):
        return [a.strip() for a in self.activities.splitlines() if a.strip()]

    @property
    def meals_display(self):
        return dict(self.MEAL_CHOICES).get(self.meals, '')

    def __str__(self):
        return f"{self.package.name} - Day {self.day_number}: {self.title}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'package'], name='unique_user_package_review')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.package.name} ({self.rating}★)"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'package'], name='unique_user_package_wishlist')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.package.name}"


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_percent = models.PositiveIntegerField(default=10)
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        today = timezone.localdate()
        return self.is_active and self.valid_from <= today <= self.valid_to

    def __str__(self):
        return self.code


class Enquiry(models.Model):
    VACATION_TYPES = [
        ('holiday', 'Holiday'),
        ('honeymoon', 'Honeymoon'),
        ('family', 'Family'),
        ('adventure', 'Adventure'),
        ('corporate', 'Corporate'),
        ('educational', 'Educational'),
        ('custom', 'Custom Trip'),
    ]
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    whatsapp = models.CharField(max_length=30, blank=True)
    destination = models.CharField(max_length=150)
    travel_date = models.DateField(null=True, blank=True)
    travelers = models.PositiveIntegerField(default=1)
    vacation_type = models.CharField(max_length=30, choices=VACATION_TYPES, default='holiday')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('new', 'New'), ('contacted', 'Contacted'), ('converted', 'Converted'), ('closed', 'Closed')
    ], default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.destination}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    message = models.TextField()
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
