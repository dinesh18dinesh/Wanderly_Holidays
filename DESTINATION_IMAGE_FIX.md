# Destination + Package Image Fix

Fixed the missing CITY_POOLS error in seed_data.py.

Destination galleries remain destination-specific (five images per destination).
Package galleries remain package/destination-specific (five images per package).

Run:
python manage.py seed_data
python manage.py runserver
