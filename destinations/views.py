from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.utils import timezone

from .forms import EnquiryForm, NewsletterForm, ReviewForm
from .models import BlogPost, Destination, Enquiry, Review, Testimonial, TravelPackage, Wishlist


def home(request):
    featured_destinations = Destination.objects.filter(is_featured=True)[:8]
    if not featured_destinations.exists():
        featured_destinations = Destination.objects.all()[:8]

    featured_packages = TravelPackage.objects.filter(is_featured=True).select_related('destination')[:8]
    if not featured_packages.exists():
        featured_packages = TravelPackage.objects.all().select_related('destination')[:8]

    testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    blogs = BlogPost.objects.filter(is_published=True)[:3]

    return render(request, 'destinations/home.html', {
        'featured_destinations': featured_destinations,
        'featured_packages': featured_packages,
        'testimonials': testimonials,
        'blogs': blogs,
        'enquiry_form': EnquiryForm(),
    })


def destination_list(request):
    destinations = Destination.objects.all()
    query = request.GET.get('q', '').strip()
    country = request.GET.get('country', '').strip()

    if query:
        destinations = destinations.filter(
            Q(name__icontains=query) | Q(city__icontains=query) | Q(country__icontains=query)
        )
    if country:
        destinations = destinations.filter(country__iexact=country)

    countries = Destination.objects.values_list('country', flat=True).distinct().order_by('country')
    page_obj = Paginator(destinations, 12).get_page(request.GET.get('page'))

    return render(request, 'destinations/destination_list.html', {
        'page_obj': page_obj, 'query': query, 'country': country, 'countries': countries
    })


def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    packages = destination.packages.all()
    return render(request, 'destinations/destination_detail.html', {
        'destination': destination, 'packages': packages
    })




def package_search_api(request):
    """Return live package suggestions for the homepage search box."""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'query': '', 'count': 0, 'packages': [], 'available': False})

    europe_countries = ['France', 'Switzerland', 'United Kingdom', 'Italy', 'Greece', 'Spain', 'Netherlands', 'Czech Republic', 'Austria', 'Hungary', 'Portugal', 'Iceland', 'Norway', 'Croatia']
    search_filter = (
        Q(name__icontains=query) |
        Q(destination__name__icontains=query) |
        Q(destination__city__icontains=query) |
        Q(destination__country__icontains=query) |
        Q(package_type__icontains=query) |
        Q(tour_type__icontains=query) |
        Q(highlights__icontains=query)
    )
    if query.lower() in {'europe', 'european', 'eu'}:
        search_filter |= Q(destination__country__in=europe_countries)

    packages = (
        TravelPackage.objects
        .select_related('destination')
        .filter(search_filter)
        .order_by('-is_featured', 'name')
        .distinct()
    )

    results = []
    for package in packages[:8]:
        results.append({
            'name': package.name,
            'slug': package.slug,
            'url': package.get_absolute_url(),
            'destination': f'{package.destination.name}, {package.destination.country}',
            'city': package.destination.city,
            'duration': f'{package.duration_days} Days',
            'price': str(package.effective_price),
            'package_type': package.get_package_type_display(),
            'image': package.image_src or '',
        })

    return JsonResponse({
        'query': query,
        'count': packages.count(),
        'packages': results,
        'available': bool(results),
    })


def package_list(request):
    packages = TravelPackage.objects.select_related('destination').all()
    query = request.GET.get('q', '').strip()
    package_type = request.GET.get('type', '').strip()
    sort = request.GET.get('sort', 'popular')
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    duration = request.GET.get('duration', '').strip()

    if query:
        packages = packages.filter(
            Q(name__icontains=query) |
            Q(destination__name__icontains=query) |
            Q(destination__city__icontains=query) |
            Q(destination__country__icontains=query)
        )
    if package_type:
        packages = packages.filter(package_type=package_type)
    if min_price:
        packages = packages.filter(discount_price__gte=min_price) | packages.filter(discount_price__isnull=True, price__gte=min_price)
    if max_price:
        packages = packages.filter(discount_price__lte=max_price) | packages.filter(discount_price__isnull=True, price__lte=max_price)
    if duration:
        packages = packages.filter(duration_days=duration)

    if sort == 'price_low':
        packages = packages.order_by('discount_price', 'price')
    elif sort == 'price_high':
        packages = packages.order_by('-discount_price', '-price')
    elif sort == 'duration':
        packages = packages.order_by('duration_days')
    else:
        packages = packages.order_by('-is_featured', '-created_at')

    page_obj = Paginator(packages, 12).get_page(request.GET.get('page'))
    return render(request, 'destinations/package_list.html', {
        'page_obj': page_obj,
        'package_types': TravelPackage.PACKAGE_TYPES,
        'selected_type': package_type,
        'sort': sort,
    })


def package_detail(request, slug):
    package = get_object_or_404(TravelPackage.objects.select_related('destination'), slug=slug)
    reviews = package.reviews.filter(is_approved=True)
    review_form = ReviewForm()
    user_has_booked = False
    is_wishlisted = False

    if request.user.is_authenticated:
        from bookings.models import Booking
        user_has_booked = Booking.objects.filter(
            user=request.user, package=package, status__in=['confirmed', 'completed']
        ).exists()
        is_wishlisted = Wishlist.objects.filter(user=request.user, package=package).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={package.get_absolute_url()}')
        if not user_has_booked:
            messages.warning(request, 'Please complete a booking before submitting a review.')
        else:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                Review.objects.update_or_create(
                    user=request.user, package=package,
                    defaults={
                        'rating': review_form.cleaned_data['rating'],
                        'comment': review_form.cleaned_data['comment'],
                        'is_approved': False
                    }
                )
                messages.success(request, 'Thank you! Your review is awaiting approval.')
                return redirect('package_detail', slug=slug)

    return render(request, 'destinations/package_detail.html', {
        'package': package,
        'reviews': reviews,
        'avg_rating': reviews.aggregate(Avg('rating'))['rating__avg'] or 0,
        'user_has_booked': user_has_booked,
        'is_wishlisted': is_wishlisted,
        'review_form': review_form,
    })


@login_required
def toggle_wishlist(request, slug):
    package = get_object_or_404(TravelPackage, slug=slug)
    item, created = Wishlist.objects.get_or_create(user=request.user, package=package)
    if created:
        messages.success(request, 'Added to your wishlist.')
    else:
        item.delete()
        messages.info(request, 'Removed from your wishlist.')
    return redirect(request.META.get('HTTP_REFERER') or package.get_absolute_url())


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related('package', 'package__destination')
    return render(request, 'destinations/wishlist.html', {'items': items})


def enquiry(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks! Our travel expert will contact you shortly.')
            return redirect('enquiry')
    else:
        form = EnquiryForm()
    return render(request, 'destinations/enquiry.html', {'form': form})


def contact(request):
    return render(request, 'destinations/contact.html')


def newsletter_subscribe(request):
    if request.method != 'POST':
        return redirect('home')
    form = NewsletterForm(request.POST)
    if form.is_valid():
        NewsletterForm.Meta.model.objects.update_or_create(
            email=form.cleaned_data['email'],
            defaults={'is_active': True}
        )
        messages.success(request, 'You are subscribed to our travel updates.')
    else:
        messages.error(request, 'Please enter a valid email address.')
    return redirect(request.META.get('HTTP_REFERER') or 'home')


def blog(request):
    posts = BlogPost.objects.filter(is_published=True)
    page_obj = Paginator(posts, 9).get_page(request.GET.get('page'))
    return render(request, 'destinations/blog.html', {'page_obj': page_obj})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'destinations/blog_detail.html', {'post': post})
