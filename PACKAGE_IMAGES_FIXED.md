# Wanderly Holidays – Package Image Fix

Every package now uses destination-specific real image URLs.

- Package cover: based on the package's catalogue image and destination.
- Gallery: 5 different images selected from that destination's image pool.
- Dubai packages use Dubai images.
- Manali packages use Manali/Himalayan images.
- Kerala packages use Kerala/backwater/nature images.
- European packages use images matched to their city/region.
- Generic LoremFlickr image searching has been removed because it was causing
  failed/blank image loads and repeated/unrelated results.

No database migration is required because this change only updates image data
and the existing model properties.
