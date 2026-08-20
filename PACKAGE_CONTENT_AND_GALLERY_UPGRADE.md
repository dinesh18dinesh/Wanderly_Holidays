# Package Content & Gallery Upgrade

Updated the Wanderly Holidays catalogue so package detail pages show clearer customer-facing inclusions.

## Included wording

Each seeded package now uses:
- A named hotel/resort property
- Daily breakfast
- Train tickets where a scheduled train journey is listed in the itinerary
- Local sightseeing tickets for listed sightseeing
- Transport by car / bus / van based on group size and itinerary
- Selected excursions listed in the itinerary
- Travel insurance

Lunch/dinner are not added as generic meal inclusions. Existing package-specific experiences (for example a cruise, spa session or desert safari) are retained when already part of the package.

## Gallery upgrade

Every package now receives **5 different gallery images**:
1. Package cover image
2. Supporting travel image 1
3. Supporting travel image 2
4. Supporting travel image 3
5. Supporting travel image 4

The gallery is generated deterministically per package, so different packages receive different supporting-image combinations instead of the old repeated fallback images.

## Run after copying/updating the project

```powershell
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

The `seed_data` command updates existing packages as well as new demo packages.
