# Package Image Search Upgrade

Every travel package now receives five destination/theme-specific image-search URLs.

- Cover image: unique per package
- Gallery: 5 different images per package
- Search uses the package destination and travel style (beach, adventure, cultural, honeymoon, family, luxury, etc.)
- Stable lock values keep the selected images different between package records
- Run `python manage.py seed_data` after extracting the project to refresh the existing database records

The image service is external, so an internet connection is required while viewing remote package images.
