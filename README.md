# Wanderly Travel & Holidays — GT Holidays-inspired upgrade

This project is a Django travel portal redesigned around common UX patterns found on large Indian travel-agency websites, especially GT Holidays: destination discovery, holiday themes, curated package cards, personalised trip enquiries, traveller reviews, travel guides, booking/payment flow and customer support.

> This is an independent project. It does not copy GT Holidays branding, source code, images, text or trademarks.

## Main upgrades

- Modern travel-agency homepage with hero search
- Holiday themes: Honeymoon, Family, Adventure, Luxury, Cultural, Wildlife, Educational and Corporate
- India/international destination discovery
- Advanced package search, filters, price range, duration and sorting
- Package detail page with:
  - pricing/discount
  - itinerary
  - highlights
  - inclusions/exclusions
  - tour type/group size/languages
  - ratings and approved reviews
  - wishlist
  - booking CTA
- Personalised **Plan My Trip** enquiry form
- Contact page
- Blog / Travel Guide with admin-managed articles
- Testimonials managed from Django Admin
- Newsletter subscriber management
- Coupon validation and discount calculation during booking
- Customer booking dashboard
- Booking cancellation
- PDF invoice
- Email confirmation
- Razorpay demo mode for development
- Razorpay signature verification for real payments
- Better admin search/filtering
- Responsive Bootstrap 5 design
- Improved visual hierarchy and mobile layout

## Reference

The feature direction was informed by publicly visible GT Holidays website patterns such as package categories, destination/package discovery, personalised holiday enquiries, honeymoon sections, reviews, blogs and travel support.

Official reference: https://www.gtholidays.in/

## Setup

Use Python 3.12 for the supplied requirements.

```powershell
cd "YOUR\Travel_Tourism_Website_Django\travelwebsite_project"

py -3.12 -m venv travel_env
.\travel_env\Scripts\Activate.ps1

python -m pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:

- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Environment

Create `.env` in the project root if required:

```env
DJANGO_SECRET_KEY=change-this
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

If Razorpay keys are empty, the website automatically uses **demo payment mode**.

For real payments, add valid Razorpay test/live credentials and keep the signature-verification endpoint enabled.

## Admin content to add first

1. Destinations
2. Travel Packages
3. Testimonials
4. Blog Posts
5. Coupons

For the best homepage result, mark several destinations and packages as **Featured**.

## Important

The ZIP contains source code changes. Run `makemigrations` and `migrate` after replacing the old project files because new database fields/models were added.

## Advanced booking & traveller management

This version includes an expanded catalogue (40+ package records after seeding) and a multi-traveller booking workflow.

### Customer account details
Registration collects name, email, phone, date of birth, gender, address, city, state, country, pincode and newsletter preference. The profile page can update these details later.

### Family & friends
Users can save reusable traveller profiles from **My Travellers**. A saved profile can be quick-filled during package checkout. Traveller records include relation, DOB, gender, nationality, contact information and optional passport/ID information.

### Booking management
A single account can book a package for themselves and multiple family members/friends. After booking, **My Bookings → Edit Trip** lets the customer correct the travel date, contact information, special requests and traveller details. Unpaid bookings can also change the traveller count when seats are available. Paid bookings keep the traveller count locked to avoid an unpaid balance/refund mismatch.

### Setup
From the folder containing `manage.py`:

```powershell
py -3.12 -m venv travel_env
.\travel_env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations destinations accounts bookings payments
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

The seed command creates/updates the travel catalogue and package information.
