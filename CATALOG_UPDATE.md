# Expanded Holiday Catalogue

This version expands the demo catalogue to 18 destinations and 23 detailed holiday packages.

## New catalogue features
- Remote cover image URLs for destinations and packages.
- Package gallery URLs (one image per line).
- Detailed descriptions, highlights, inclusions, exclusions and day-wise itineraries.
- Tour type, group size, languages, seats, pricing and discount pricing.
- Honeymoon, family, beach, adventure, cultural and luxury packages.
- Existing uploaded `main_image`/destination `image` files always take priority over remote URLs.

## Load the catalogue
From the folder containing `manage.py`:

```powershell
python manage.py makemigrations destinations
python manage.py migrate
python manage.py seed_data
```

Then run:

```powershell
python manage.py runserver
```

The image URLs require an internet connection in the browser. You can replace any remote image with a permanent uploaded image from Django Admin.
