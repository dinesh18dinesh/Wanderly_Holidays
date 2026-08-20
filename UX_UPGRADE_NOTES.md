# Wanderly Holidays — UX View Upgrade

This version keeps the existing signup/login and booking/payment flow and upgrades the travel discovery experience.

## Main upgrades

- Premium package detail page
- Clickable package image gallery with previous/next controls and fullscreen lightbox
- Sticky package navigation
- Responsive mobile Book Now bar
- Package overview and highlights
- Visual day-by-day itinerary
- Included services and a dedicated Travel Insurance included panel
- Outside-this-package information
- Package travel guide
- Reviews and FAQ accordion
- Related package recommendations
- Destination detail page with clickable image gallery
- Destination highlights, things to do, planning guide and package discovery
- Admin fields for destination gallery/highlights/travel guide
- Admin fields for package travel guide, FAQs and insurance inclusion
- Seed data updated so travel insurance is included in the package catalogue

## Run

From `travelwebsite_project`:

```powershell
# Activate your existing environment
.	ravel_env\Scripts\Activate.ps1

python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

The bundled `db.sqlite3` has also been updated with the new fields so the supplied demo database matches the new models.

## Important

The original signup and booking templates were intentionally preserved. The main UX work is concentrated on package and destination view pages.
