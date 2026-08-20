from django.core.management.base import BaseCommand
from hashlib import md5
from destinations.models import Destination, ItineraryDay, TravelPackage

IMG = 'https://images.unsplash.com/{id}?auto=format&fit=crop&w=1400&q=85'

DESTINATION_GALLERIES = {'Goa': ['https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1400&q=88',
         'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1400&q=88',
         'https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1400&q=88',
         'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1400&q=88',
         'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1400&q=88'],
 'Manali': ['https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1470214304380-aadaedcfff1b?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1400&q=88'],
 'Alleppey': ['https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1593693411515-c20261bcad6e?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1511497584788-876760111969?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1501854140801-50d01698950b?auto=format&fit=crop&w=1400&q=88'],
 'Jaipur': ['https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1519817650390-64a93db51149?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1523480717984-24cba35ae1ef?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1521292270410-a8c4d716d518?auto=format&fit=crop&w=1400&q=88'],
 'Agra': ['https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1519817650390-64a93db51149?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1523480717984-24cba35ae1ef?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1400&q=88'],
 'Srinagar': ['https://images.unsplash.com/photo-1605649487212-47bdab064df7?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1582972236019-ea9f0c9a8c1f?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1400&q=88'],
 'Leh': ['https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1400&q=88',
         'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1400&q=88',
         'https://images.unsplash.com/photo-1470214304380-aadaedcfff1b?auto=format&fit=crop&w=1400&q=88',
         'https://images.unsplash.com/photo-1528127269322-539801943592?auto=format&fit=crop&w=1400&q=88',
         'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1400&q=88'],
 'Mysuru': ['https://images.unsplash.com/photo-1590050752117-23a9d2c8a4d3?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1519817650390-64a93db51149?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1523480717984-24cba35ae1ef?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1400&q=88'],
 'Kodaikanal': ['https://images.unsplash.com/photo-1582610116397-edb318620f90?auto=format&fit=crop&w=1400&q=88',
                'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1400&q=88',
                'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1400&q=88',
                'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1400&q=88',
                'https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1400&q=88'],
 'Ooty': ['https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1400&q=88'],
 'Port Blair': ['https://images.unsplash.com/photo-1540202404-a2f29016b523?auto=format&fit=crop&w=1400&q=88',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1400&q=88',
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1400&q=88',
                'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1400&q=88',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1400&q=88'],
 'Dubai': ['https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1400&q=88',
           'https://images.unsplash.com/photo-1518684079-3c830dcef090?auto=format&fit=crop&w=1400&q=88',
           'https://images.unsplash.com/photo-1527631746610-bca00a040d60?auto=format&fit=crop&w=1400&q=88',
           'https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1400&q=88',
           'https://images.unsplash.com/photo-1533929736458-ca588d08c8be?auto=format&fit=crop&w=1400&q=88'],
 'Denpasar': ['https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1539367628448-4bc5c9d171c8?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1400&q=88'],
 'Malé': ['https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1511497584788-876760111969?auto=format&fit=crop&w=1400&q=88'],
 'Singapore': ['https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1527631746610-bca00a040d60?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1521292270410-a8c4d716d518?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1533929736458-ca588d08c8be?auto=format&fit=crop&w=1400&q=88'],
 'Paris': ['https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1400&q=88',
           'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=1400&q=88',
           'https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?auto=format&fit=crop&w=1400&q=88',
           'https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1400&q=88',
           'https://images.unsplash.com/photo-1523480717984-24cba35ae1ef?auto=format&fit=crop&w=1400&q=88'],
 'Interlaken': ['https://images.unsplash.com/photo-1527668752968-14dc70a27c95?auto=format&fit=crop&w=1400&q=88',
                'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1400&q=88',
                'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1400&q=88',
                'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1400&q=88',
                'https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1400&q=88'],
 'London': ['https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1533929736458-ca588d08c8be?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1521292270410-a8c4d716d518?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=1400&q=88'],
 'Rome': ['https://images.unsplash.com/photo-1529260830199-42c24126f198?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1400&q=88',
          'https://images.unsplash.com/photo-1523480717984-24cba35ae1ef?auto=format&fit=crop&w=1400&q=88'],
 'Santorini': ['https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1400&q=88'],
 'Zurich': ['https://images.unsplash.com/photo-1521292270410-a8c4d716d518?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1527668752968-14dc70a27c95?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1528127269322-539801943592?auto=format&fit=crop&w=1400&q=88'],
 'Barcelona': ['https://images.unsplash.com/photo-1539037116277-4db20889f2d4?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1523480717984-24cba35ae1ef?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1400&q=88'],
 'Amsterdam': ['https://images.unsplash.com/photo-1534351590666-13e3e96b5017?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1521292270410-a8c4d716d518?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1533929736458-ca588d08c8be?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=1400&q=88'],
 'Prague': ['https://images.unsplash.com/photo-1541849546-216549ae216d?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1521292270410-a8c4d716d518?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1533929736458-ca588d08c8be?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=1400&q=88'],
 'Vienna': ['https://images.unsplash.com/photo-1516550893923-42d28e5677af?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1521292270410-a8c4d716d518?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1533929736458-ca588d08c8be?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=1400&q=88'],
 'Budapest': ['https://images.unsplash.com/photo-1541849546-216549ae216d?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1521292270410-a8c4d716d518?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1533929736458-ca588d08c8be?auto=format&fit=crop&w=1400&q=88',
              'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=1400&q=88'],
 'Lisbon': ['https://images.unsplash.com/photo-1555881400-74d7acaacd8b?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1521292270410-a8c4d716d518?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1533929736458-ca588d08c8be?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=1400&q=88'],
 'Reykjavik': ['https://images.unsplash.com/photo-1520769945061-0a448c463865?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1400&q=88'],
 'Bergen': ['https://images.unsplash.com/photo-1531366936337-7c912a4589a7?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1528127269322-539801943592?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1400&q=88',
            'https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1400&q=88'],
 'Dubrovnik': ['https://images.unsplash.com/photo-1555993539-1732b0258235?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1528127269322-539801943592?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1400&q=88',
               'https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1400&q=88']}


DESTINATIONS = [
    ('Goa Beaches', 'Goa', 'India', 'Golden beaches, Portuguese heritage, island cruises and vibrant coastal nightlife.', 15.2993, 74.1240, 'Nov - Feb', True, IMG.format(id='photo-1512343879784-a960bf40e7f2')),
    ('Manali Hills', 'Manali', 'India', 'Snow-capped Himalayan peaks, valleys, cafes, trekking and adventure experiences.', 32.2432, 77.1892, 'Mar - Jun, Oct - Feb', True, IMG.format(id='photo-1506905925346-21bda4d32df4')),
    ('Kerala Backwaters', 'Alleppey', 'India', 'Peaceful houseboats, coconut-lined waterways, Ayurveda and slow travel in Kerala.', 9.4981, 76.3388, 'Sep - Mar', True, IMG.format(id='photo-1602216056096-3b40cc0c9944')),
    ('Royal Jaipur', 'Jaipur', 'India', 'The Pink City with royal palaces, colourful bazaars, forts and rich Rajasthani cuisine.', 26.9124, 75.7873, 'Oct - Mar', True, IMG.format(id='photo-1599661046289-e31897846e41')),
    ('Agra Taj Mahal', 'Agra', 'India', 'A heritage escape centred around the Taj Mahal, Agra Fort and Mughal history.', 27.1767, 78.0081, 'Oct - Mar', False, IMG.format(id='photo-1564507592333-c60657eea523')),
    ('Kashmir Valley', 'Srinagar', 'India', 'Lakes, mountain valleys, gardens and unforgettable Himalayan scenery.', 34.0837, 74.7973, 'Apr - Oct', True, IMG.format(id='photo-1605649487212-47bdab064df7')),
    ('Ladakh Adventure', 'Leh', 'India', 'High-altitude landscapes, monasteries, mountain passes and road-trip adventures.', 34.1526, 77.5771, 'May - Sep', False, IMG.format(id='photo-1544735716-392fe2489ffa')),
    ('Mysore Heritage', 'Mysuru', 'India', 'Palaces, gardens, local cuisine and the elegant heritage of Karnataka.', 12.2958, 76.6394, 'Oct - Feb', False, IMG.format(id='photo-1601050690597-df0568f70950')),
    ('Kodaikanal Escape', 'Kodaikanal', 'India', 'Misty hills, pine forests, viewpoints and a relaxing Tamil Nadu hill-station break.', 10.2381, 77.4892, 'Apr - Jun, Sep - Oct', False, IMG.format(id='photo-1582610116397-edb318620f90')),
    ('Ooty & Nilgiris', 'Ooty', 'India', 'Tea estates, toy trains, botanical gardens and cool mountain air.', 11.4102, 76.6950, 'Mar - Jun', False, IMG.format(id='photo-1597074866923-dc0589150358')),
    ('Andaman Islands', 'Port Blair', 'India', 'Turquoise water, coral reefs, island beaches and water-sports adventures.', 11.6234, 92.7265, 'Oct - May', True, IMG.format(id='photo-1540202404-a2f29016b523')),
    ('Dubai City', 'Dubai', 'UAE', 'Luxury shopping, desert safaris, skyline experiences and family attractions.', 25.2048, 55.2708, 'Nov - Mar', True, IMG.format(id='photo-1512453979798-5ea266f8880c')),
    ('Bali Paradise', 'Denpasar', 'Indonesia', 'Tropical beaches, temples, rice terraces and wellness experiences across Bali.', -8.6500, 115.2167, 'Apr - Oct', True, IMG.format(id='photo-1537996194471-e657df975ab4')),
    ('Maldives Escape', 'Malé', 'Maldives', 'Private islands, lagoons, overwater stays and romantic tropical experiences.', 4.1755, 73.5093, 'Nov - Apr', True, IMG.format(id='photo-1514282401047-d79a71a590e8')),
    ('Singapore Explorer', 'Singapore', 'Singapore', 'A modern city break featuring Gardens by the Bay, Sentosa and iconic food districts.', 1.3521, 103.8198, 'Feb - Apr', False, IMG.format(id='photo-1525625293386-3f8f99389edd')),
    ('Paris & France', 'Paris', 'France', 'Art, architecture, cuisine and romantic European city experiences.', 48.8566, 2.3522, 'Apr - Jun, Sep - Oct', True, IMG.format(id='photo-1502602898657-3e91760cbb34')),
    ('Swiss Alps', 'Interlaken', 'Switzerland', 'Alpine villages, panoramic rail journeys, lakes and mountain excursions.', 46.6863, 7.8632, 'Jun - Sep', True, IMG.format(id='photo-1527668752968-14dc70a27c95')),
    ('London Highlights', 'London', 'United Kingdom', 'Royal landmarks, museums, shopping districts and classic British experiences.', 51.5074, -0.1278, 'May - Sep', False, IMG.format(id='photo-1513635269975-59663e0ac1ad')),
]

PACKAGES = [
    dict(name='Goa Beach Getaway', city='Goa', days=4, price=15999, sale=12999, type='beach', tour='private', group='2-10', langs='English, Hindi, Tamil', featured=True, seats=18,
         desc='A relaxed coastal holiday covering Goa beaches, Old Goa heritage and a choice of water activities.', highlights='Baga & Calangute beaches\nOld Goa heritage walk\nSunset cruise\nOptional water sports', inc='Hotel stay, Breakfast, Airport transfer, Sightseeing, Sunset cruise', exc='Flights, Alcohol, Personal expenses, Optional water sports', itinerary='Day 1: Arrival and beach relaxation\nDay 2: North Goa beaches and water sports\nDay 3: Old Goa churches, Panjim and sunset cruise\nDay 4: Breakfast and departure', image=IMG.format(id='photo-1512343879784-a960bf40e7f2')),
    dict(name='Goa Premium Honeymoon', city='Goa', days=5, price=32999, sale=27999, type='honeymoon', tour='private', group='2-4', langs='English, Hindi, Tamil', featured=True, seats=10,
         desc='A romantic Goa escape with premium resort stays, candlelight dining and private sightseeing.', highlights='Premium beach resort\nCouple photoshoot\nCandlelight dinner\nPrivate sunset cruise', inc='Premium stay, Breakfast, Private transfers, Candlelight dinner, Cruise', exc='Flights, Personal shopping, Alcohol', itinerary='Day 1: Arrival and resort check-in\nDay 2: Beach leisure and couple photoshoot\nDay 3: South Goa sightseeing\nDay 4: Private sunset cruise and dinner\nDay 5: Departure', image=IMG.format(id='photo-1500530855697-b586d89ba3ee')),
    dict(name='Manali Adventure Trek', city='Manali', days=5, price=18999, sale=15999, type='adventure', tour='group', group='4-16', langs='English, Hindi', featured=True, seats=16,
         desc='A Himalayan adventure combining scenic valleys, trekking, camping and river activities.', highlights='Solang Valley\nGuided trek\nRiverside camping\nRiver rafting option', inc='Hotel stay, Camping, Trek guide, Breakfast, Equipment, Transfers', exc='Travel insurance, Personal gear, Optional rafting', itinerary='Day 1: Arrival and acclimatisation\nDay 2: Solang Valley adventure\nDay 3: Guided mountain trek and camp\nDay 4: River activity and local market\nDay 5: Departure', image=IMG.format(id='photo-1506905925346-21bda4d32df4')),
    dict(name='Manali Family Holiday', city='Manali', days=6, price=24999, sale=21999, type='family', tour='private', group='2-8', langs='English, Hindi, Tamil', featured=True, seats=20,
         desc='Family-friendly Himalayan sightseeing with comfortable stays, easy activities and flexible free time.', highlights='Hadimba Temple\nSolang Valley\nMall Road\nFamily-friendly sightseeing', inc='Hotel, Breakfast, Private cab, Driver, Sightseeing', exc='Lunch and dinner, Adventure activities, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Local Manali sightseeing\nDay 3: Solang Valley\nDay 4: Naggar and village experience\nDay 5: Leisure and shopping\nDay 6: Departure', image=IMG.format(id='photo-1476514525535-07fb3b4ae5f1')),
    dict(name='Kerala Houseboat Bliss', city='Alleppey', days=3, price=13999, sale=10999, type='cultural', tour='private', group='2-6', langs='English, Malayalam, Tamil', featured=True, seats=14,
         desc='A serene Kerala journey featuring a private houseboat, village life and local cuisine.', highlights='Private houseboat\nBackwater cruise\nVillage visit\nKerala cuisine', inc='Houseboat stay, All meals, Village tour, Transfers', exc='Flights, Tips, Alcohol', itinerary='Day 1: Arrival in Alleppey and houseboat check-in\nDay 2: Backwater cruise and village visit\nDay 3: Breakfast and departure', image=IMG.format(id='photo-1602216056096-3b40cc0c9944')),
    dict(name='Kerala Honeymoon Retreat', city='Alleppey', days=5, price=35999, sale=30999, type='honeymoon', tour='private', group='2', langs='English, Malayalam, Tamil', featured=True, seats=8,
         desc='A romantic Kerala itinerary combining Munnar tea hills, Alleppey backwaters and premium stays.', highlights='Munnar tea gardens\nPrivate houseboat\nCouple spa\nCandlelight dinner', inc='Premium hotels, Breakfast, Houseboat, Private transfers, Dinner', exc='Flights, Personal expenses, Optional activities', itinerary='Day 1: Kochi to Munnar\nDay 2: Munnar sightseeing\nDay 3: Munnar to Alleppey\nDay 4: Private houseboat and romantic dinner\nDay 5: Departure', image=IMG.format(id='photo-1593693411515-c20261bcad6e')),
    dict(name='Royal Jaipur Heritage', city='Jaipur', days=3, price=11999, sale=9999, type='cultural', tour='private', group='2-10', langs='English, Hindi, Tamil', featured=True, seats=22,
         desc='Discover Jaipur through royal forts, palaces, bazaars and traditional Rajasthani flavours.', highlights='Amber Fort\nCity Palace\nHawa Mahal\nLocal bazaar walk', inc='Hotel, Breakfast, Private cab, Guide, Monument entries', exc='Lunch/Dinner, Shopping, Personal expenses', itinerary='Day 1: Amber Fort and Jal Mahal\nDay 2: City Palace, Jantar Mantar and Hawa Mahal\nDay 3: Bazaar visit and departure', image=IMG.format(id='photo-1599661046289-e31897846e41')),
    dict(name='Agra Taj Mahal Sunrise', city='Agra', days=2, price=7999, sale=6999, type='cultural', tour='private', group='2-8', langs='English, Hindi', featured=False, seats=20,
         desc='A compact heritage break focused on the Taj Mahal at sunrise and Agra Fort.', highlights='Taj Mahal sunrise\nAgra Fort\nLocal craft experience', inc='Hotel, Breakfast, Private cab, Monument entries, Guide', exc='Lunch/Dinner, Camera fees, Shopping', itinerary='Day 1: Arrival and Agra Fort\nDay 2: Taj Mahal sunrise, breakfast and departure', image=IMG.format(id='photo-1564507592333-c60657eea523')),
    dict(name='Kashmir Paradise Tour', city='Srinagar', days=6, price=29999, sale=25999, type='family', tour='private', group='2-8', langs='English, Hindi, Tamil', featured=True, seats=16,
         desc='A scenic Kashmir holiday with Srinagar, Gulmarg, Pahalgam and a relaxing shikara experience.', highlights='Dal Lake shikara\nGulmarg excursion\nPahalgam valley\nMughal gardens', inc='Hotel/houseboat, Breakfast, Private cab, Shikara ride, Sightseeing', exc='Gondola tickets, Flights, Personal expenses', itinerary='Day 1: Srinagar arrival and shikara ride\nDay 2: Srinagar gardens and old city\nDay 3: Gulmarg excursion\nDay 4: Pahalgam excursion\nDay 5: Leisure and shopping\nDay 6: Departure', image=IMG.format(id='photo-1605649487212-47bdab064df7')),
    dict(name='Ladakh Bike Adventure', city='Leh', days=7, price=42999, sale=38999, type='adventure', tour='group', group='4-12', langs='English, Hindi', featured=False, seats=12,
         desc='An adventurous Ladakh circuit across dramatic high-altitude passes, monasteries and mountain roads.', highlights='Khardung La region\nPangong Lake\nMonastery visits\nScenic mountain drive', inc='Hotel/camp, Breakfast, Bike, Fuel allowance, Permits, Support vehicle', exc='Flights, Riding gear, Insurance, Personal expenses', itinerary='Day 1: Leh arrival and rest\nDay 2: Leh local monasteries\nDay 3: Khardung La region\nDay 4: Nubra Valley\nDay 5: Pangong Lake\nDay 6: Return to Leh\nDay 7: Departure', image=IMG.format(id='photo-1544735716-392fe2489ffa')),
    dict(name='Mysore Royal Weekend', city='Mysuru', days=2, price=6999, sale=5999, type='cultural', tour='private', group='2-8', langs='English, Kannada, Tamil', featured=False, seats=25,
         desc='A short heritage break exploring Mysore Palace, markets and nearby cultural landmarks.', highlights='Mysore Palace\nChamundi Hill\nDevaraja Market\nLocal cuisine', inc='Hotel, Breakfast, Private cab, Sightseeing', exc='Lunch/Dinner, Entry upgrades, Shopping', itinerary='Day 1: Palace, market and city tour\nDay 2: Chamundi Hill and departure', image=IMG.format(id='photo-1601050690597-df0568f70950')),
    dict(name='Kodaikanal Misty Escape', city='Kodaikanal', days=3, price=8999, sale=7499, type='family', tour='private', group='2-8', langs='English, Tamil', featured=False, seats=20,
         desc='A peaceful hill-station escape with lakes, viewpoints, pine forests and relaxed sightseeing.', highlights='Kodaikanal Lake\nCoaker’s Walk\nPine forest\nPillar Rocks', inc='Hotel, Breakfast, Private cab, Sightseeing', exc='Lunch/Dinner, Boating, Personal expenses', itinerary='Day 1: Arrival and lake area\nDay 2: Viewpoints and pine forest\nDay 3: Leisure and departure', image=IMG.format(id='photo-1582610116397-edb318620f90')),
    dict(name='Ooty Tea & Toy Train', city='Ooty', days=3, price=9999, sale=8499, type='family', tour='private', group='2-8', langs='English, Tamil', featured=False, seats=18,
         desc='A cool Nilgiri holiday featuring tea estates, gardens and a memorable toy-train experience.', highlights='Nilgiri toy train\nTea estate visit\nBotanical Garden\nDoddabetta Peak', inc='Hotel, Breakfast, Private cab, Sightseeing, Tea estate visit', exc='Toy train tickets subject to availability, Lunch/Dinner', itinerary='Day 1: Arrival and Ooty town\nDay 2: Tea estate, Doddabetta and gardens\nDay 3: Leisure and departure', image=IMG.format(id='photo-1597074866923-dc0589150358')),
    dict(name='Andaman Island Explorer', city='Port Blair', days=6, price=32999, sale=28999, type='beach', tour='private', group='2-8', langs='English, Hindi, Tamil', featured=True, seats=14,
         desc='Island hopping with beaches, coral reefs, water activities and historic landmarks.', highlights='Havelock Island\nRadhanagar Beach\nSnorkelling\nCellular Jail', inc='Hotels, Breakfast, Ferry tickets, Transfers, Sightseeing', exc='Flights, Scuba diving, Personal expenses', itinerary='Day 1: Port Blair arrival and Cellular Jail\nDay 2: Havelock transfer\nDay 3: Radhanagar Beach\nDay 4: Water activities\nDay 5: Return to Port Blair\nDay 6: Departure', image=IMG.format(id='photo-1540202404-a2f29016b523')),
    dict(name='Dubai Luxury Family', city='Dubai', days=5, price=49999, sale=42999, type='luxury', tour='private', group='2-6', langs='English, Hindi, Tamil', featured=True, seats=12,
         desc='A premium Dubai holiday with skyline views, desert safari and family attractions.', highlights='Burj Khalifa\nDesert safari\nDubai Marina cruise\nDubai Mall', inc='4-star hotel, Breakfast, Airport transfers, Desert safari, City tour', exc='Flights, Visa, Personal expenses, Optional attractions', itinerary='Day 1: Arrival and Marina evening\nDay 2: Burj Khalifa and Dubai Mall\nDay 3: Desert safari\nDay 4: Abu Dhabi or leisure day\nDay 5: Departure', image=IMG.format(id='photo-1512453979798-5ea266f8880c')),
    dict(name='Dubai Honeymoon Escape', city='Dubai', days=5, price=57999, sale=49999, type='honeymoon', tour='private', group='2', langs='English, Hindi', featured=False, seats=8,
         desc='A stylish couple holiday with luxury accommodation, private experiences and sunset views.', highlights='Luxury stay\nPrivate desert dinner\nMarina cruise\nSkyline experience', inc='5-star stay, Breakfast, Private transfers, Cruise, Desert experience', exc='Flights, Visa, Personal shopping', itinerary='Day 1: Arrival and romantic evening\nDay 2: Burj Khalifa and city tour\nDay 3: Desert safari and private dinner\nDay 4: Marina cruise and leisure\nDay 5: Departure', image=IMG.format(id='photo-1518684079-3c830dcef090')),
    dict(name='Bali Island Escape', city='Denpasar', days=6, price=45999, sale=39999, type='beach', tour='private', group='2-6', langs='English, Hindi, Tamil', featured=True, seats=15,
         desc='A balanced Bali holiday covering beaches, Ubud rice terraces, temples and wellness experiences.', highlights='Ubud rice terraces\nBeach resort\nTemple visit\nSunset experience', inc='Resort stay, Breakfast, Airport transfer, Private sightseeing, Temple visit', exc='International flights, Visa fees, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Ubud and rice terraces\nDay 3: Temple and cultural tour\nDay 4: Beach leisure\nDay 5: Water activity or spa\nDay 6: Departure', image=IMG.format(id='photo-1537996194471-e657df975ab4')),
    dict(name='Bali Romantic Honeymoon', city='Denpasar', days=7, price=69999, sale=59999, type='honeymoon', tour='private', group='2', langs='English, Hindi', featured=True, seats=8,
         desc='A romantic Bali journey with private pool stays, floating breakfast and sunset experiences.', highlights='Private pool villa\nFloating breakfast\nCouple spa\nSunset dinner', inc='Premium villa, Breakfast, Private transfers, Couple spa, Romantic dinner', exc='Flights, Visa, Personal expenses', itinerary='Day 1: Arrival and villa check-in\nDay 2: Ubud private tour\nDay 3: Spa and leisure\nDay 4: Temple and sunset\nDay 5: Beach club\nDay 6: Free day\nDay 7: Departure', image=IMG.format(id='photo-1539367628448-4bc5c9d171c8')),
    dict(name='Maldives Island Romance', city='Malé', days=5, price=79999, sale=69999, type='honeymoon', tour='private', group='2', langs='English, Hindi', featured=True, seats=8,
         desc='A tropical couple escape with an island resort, lagoon activities and romantic dining.', highlights='Overwater villa option\nSnorkelling\nSunset cruise\nPrivate beach dinner', inc='Resort stay, Breakfast, Speedboat/seaplane transfer, Activities', exc='International flights, Visa, Scuba diving, Personal expenses', itinerary='Day 1: Arrival and island transfer\nDay 2: Lagoon leisure and snorkelling\nDay 3: Spa and sunset cruise\nDay 4: Beach day and private dinner\nDay 5: Departure', image=IMG.format(id='photo-1514282401047-d79a71a590e8')),
    dict(name='Singapore Family Explorer', city='Singapore', days=5, price=39999, sale=34999, type='family', tour='private', group='2-8', langs='English, Hindi, Tamil', featured=False, seats=18,
         desc='A family-friendly city break combining Gardens by the Bay, Sentosa and iconic Singapore attractions.', highlights='Gardens by the Bay\nSentosa Island\nUniversal Studios option\nNight Safari option', inc='Hotel, Breakfast, Airport transfer, City tour, Selected attraction tickets', exc='Flights, Visa, Optional attractions, Personal expenses', itinerary='Day 1: Arrival and Marina Bay\nDay 2: Gardens by the Bay and city tour\nDay 3: Sentosa\nDay 4: Leisure or Universal Studios\nDay 5: Departure', image=IMG.format(id='photo-1525625293386-3f8f99389edd')),
    dict(name='Paris Romantic Break', city='Paris', days=5, price=69999, sale=59999, type='honeymoon', tour='private', group='2', langs='English, Hindi', featured=True, seats=10,
         desc='A classic Paris escape with iconic landmarks, Seine views, art and romantic neighbourhoods.', highlights='Eiffel Tower\nSeine cruise\nLouvre area\nMontmartre', inc='Hotel, Breakfast, Airport transfers, Seine cruise, City sightseeing', exc='International flights, Visa, Museum upgrades, Personal expenses', itinerary='Day 1: Arrival and Seine evening\nDay 2: Eiffel Tower and central Paris\nDay 3: Louvre area and historic quarters\nDay 4: Montmartre and leisure\nDay 5: Departure', image=IMG.format(id='photo-1502602898657-3e91760cbb34')),
    dict(name='Swiss Alps Scenic Journey', city='Interlaken', days=7, price=89999, sale=77999, type='luxury', tour='private', group='2-6', langs='English, Hindi', featured=True, seats=12,
         desc='A scenic Switzerland itinerary with alpine rail journeys, lakes, villages and mountain viewpoints.', highlights='Jungfraujoch\nInterlaken\nLake cruise\nScenic rail journey', inc='Hotels, Breakfast, Rail passes, Selected excursions, Transfers', exc='International flights, Visa, Travel insurance, Personal expenses', itinerary='Day 1: Arrival in Zurich and transfer\nDay 2: Lucerne\nDay 3: Interlaken\nDay 4: Jungfraujoch\nDay 5: Lake and village excursion\nDay 6: Scenic rail journey\nDay 7: Departure', image=IMG.format(id='photo-1527668752968-14dc70a27c95')),
    dict(name='London Classic Tour', city='London', days=5, price=64999, sale=55999, type='cultural', tour='private', group='2-6', langs='English, Hindi', featured=False, seats=14,
         desc='Explore London’s royal landmarks, museums, riverfront and historic neighbourhoods.', highlights='Buckingham Palace\nTower Bridge\nWestminster\nThames experience', inc='Hotel, Breakfast, Airport transfer, City tour, Selected entries', exc='Flights, Visa, Personal expenses', itinerary='Day 1: Arrival and Westminster\nDay 2: Buckingham Palace and central London\nDay 3: Tower Bridge and City of London\nDay 4: Museums and leisure\nDay 5: Departure', image=IMG.format(id='photo-1513635269975-59663e0ac1ad')),
]


# Additional catalogue packages for a larger production-style inventory.
PACKAGES.extend([
    dict(name='Goa Luxury Escape', city='Goa', days=4, price=38999, sale=32999, type='luxury', tour='private', group='2-4', langs='English, Hindi', featured=True, seats=16, desc='Premium Goa holiday with a boutique stay, sunset cruise, North Goa sightseeing and relaxed beach time.', highlights='Boutique beach resort\nSunset cruise\nNorth Goa landmarks\nPrivate transfers', inc='4-star hotel, Breakfast, Private transfers, Sunset cruise, Sightseeing', exc='Flights, Personal expenses, Water sports, Travel insurance', itinerary='Day 1: Arrival and resort check-in\nDay 2: North Goa sightseeing and beach time\nDay 3: Sunset cruise and leisure\nDay 4: Departure', image=IMG.format(id='photo-1512343879784-a960bf40e7f2')),
    dict(name='Manali Snow Adventure', city='Manali', days=6, price=41999, sale=35999, type='adventure', tour='group', group='4-12', langs='English, Hindi', featured=True, seats=20, desc='Snow-filled Himalayan adventure covering Solang Valley, local villages and mountain activities.', highlights='Solang Valley\nSnow activities\nOld Manali\nMountain cafe experience', inc='Hotel, Breakfast, Transfers, Sightseeing, Local guide', exc='Adventure activity fees, Lunch, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Old Manali and local market\nDay 3: Solang Valley\nDay 4: Atal Tunnel excursion\nDay 5: Leisure\nDay 6: Departure', image=IMG.format(id='photo-1506905925346-21bda4d32df4')),
    dict(name='Kerala Ayurveda Retreat', city='Alleppey', days=5, price=44999, sale=37999, type='luxury', tour='private', group='2-4', langs='English, Hindi', featured=True, seats=12, desc='Relaxing Kerala wellness escape with a premium houseboat stay and curated Ayurveda experiences.', highlights='Private houseboat\nAyurveda session\nBackwater cruise\nKerala cuisine', inc='Premium hotels, Houseboat, Breakfast, Ayurveda session, Transfers', exc='Flights, Personal treatments, Insurance', itinerary='Day 1: Kochi arrival\nDay 2: Alleppey houseboat\nDay 3: Ayurveda and leisure\nDay 4: Kumarakom\nDay 5: Departure', image=IMG.format(id='photo-1602216056096-3b40cc0c9944')),
    dict(name='Jaipur Udaipur Heritage Trail', city='Jaipur', days=7, price=46999, sale=39999, type='cultural', tour='private', group='2-8', langs='English, Hindi', featured=True, seats=15, desc='Royal Rajasthan circuit connecting Jaipur and the romantic lakeside heritage of Udaipur.', highlights='Amber Fort\nCity Palace\nLake Pichola\nHeritage dinner', inc='Hotels, Breakfast, Private vehicle, Sightseeing, Driver', exc='Flights, Monument fees, Personal expenses', itinerary='Day 1: Jaipur arrival\nDay 2: Amber Fort\nDay 3: Jaipur bazaars\nDay 4: Transfer to Udaipur\nDay 5: City Palace and Lake Pichola\nDay 6: Leisure\nDay 7: Departure', image=IMG.format(id='photo-1599661046289-e31897846e41')),
    dict(name='Agra Mathura Vrindavan Heritage', city='Agra', days=3, price=16999, sale=13999, type='pilgrimage', tour='private', group='2-8', langs='English, Hindi', featured=False, seats=25, desc='Short heritage and pilgrimage journey covering the Taj Mahal, Mathura and Vrindavan.', highlights='Taj Mahal\nAgra Fort\nMathura temples\nVrindavan evening', inc='Hotel, Breakfast, Transfers, Sightseeing, Driver', exc='Monument fees, Lunch, Personal expenses', itinerary='Day 1: Agra arrival and Taj Mahal\nDay 2: Agra Fort and Mathura\nDay 3: Vrindavan and departure', image=IMG.format(id='photo-1564507592333-c60657eea523')),
    dict(name='Kashmir Family Paradise', city='Srinagar', days=6, price=39999, sale=33999, type='family', tour='private', group='2-8', langs='English, Hindi', featured=True, seats=18, desc='Family-friendly Kashmir holiday with a houseboat stay, Gulmarg and Pahalgam.', highlights='Dal Lake\nGulmarg\nPahalgam\nHouseboat stay', inc='Hotels, Breakfast, Shikara ride, Transfers, Sightseeing', exc='Flights, Gondola tickets, Lunch, Personal expenses', itinerary='Day 1: Srinagar\nDay 2: Gulmarg\nDay 3: Pahalgam\nDay 4: Srinagar houseboat\nDay 5: Local sightseeing\nDay 6: Departure', image=IMG.format(id='photo-1582972236019-ea9f0c9a8c1f')),
    dict(name='Ladakh Bike Expedition', city='Leh', days=8, price=57999, sale=49999, type='adventure', tour='group', group='6-15', langs='English, Hindi', featured=True, seats=15, desc='High-altitude Ladakh adventure with monasteries, passes, lakes and guided motorcycle routes.', highlights='Khardung La\nPangong Lake\nNubra Valley\nMonasteries', inc='Hotels, Breakfast, Support vehicle, Bike, Permits', exc='Fuel, Flights, Personal expenses, Insurance', itinerary='Day 1: Leh acclimatisation\nDay 2: Leh monasteries\nDay 3: Nubra Valley\nDay 4: Khardung La\nDay 5: Pangong Lake\nDay 6: Pangong to Leh\nDay 7: Local ride\nDay 8: Departure', image=IMG.format(id='photo-1548013146-72479768bada')),
    dict(name='Mysore Coorg Coffee Trail', city='Mysore', days=4, price=21999, sale=17999, type='cultural', tour='private', group='2-6', langs='English, Hindi', featured=False, seats=20, desc='South India getaway combining Mysore Palace, Coorg coffee estates and waterfalls.', highlights='Mysore Palace\nCoorg coffee estate\nAbbey Falls\nLocal cuisine', inc='Hotel, Breakfast, Private vehicle, Sightseeing', exc='Entry tickets, Lunch, Personal expenses', itinerary='Day 1: Mysore Palace\nDay 2: Transfer to Coorg\nDay 3: Coffee estate and waterfalls\nDay 4: Departure', image=IMG.format(id='photo-1590050752117-23a9d2c8a4d3')),
    dict(name='Ooty Coonoor Family Holiday', city='Ooty', days=4, price=22999, sale=18999, type='family', tour='private', group='2-8', langs='English, Hindi', featured=False, seats=20, desc='Cool Nilgiri escape with Ooty Lake, botanical gardens and a scenic Coonoor train experience.', highlights='Ooty Lake\nBotanical Garden\nCoonoor\nTea gardens', inc='Hotel, Breakfast, Transfers, Sightseeing', exc='Toy train tickets, Lunch, Personal expenses', itinerary='Day 1: Ooty arrival\nDay 2: Ooty sightseeing\nDay 3: Coonoor and tea gardens\nDay 4: Departure', image=IMG.format(id='photo-1500534623283-312aade485b7')),
    dict(name='Andaman Island Discovery', city='Port Blair', days=6, price=45999, sale=38999, type='beach', tour='private', group='2-6', langs='English, Hindi', featured=True, seats=16, desc='Island escape featuring Havelock beaches, snorkelling, sunset views and tropical relaxation.', highlights='Radhanagar Beach\nHavelock Island\nSnorkelling\nCellular Jail', inc='Hotels, Breakfast, Ferry tickets, Transfers, Sightseeing', exc='Flights, Water sports, Personal expenses', itinerary='Day 1: Port Blair\nDay 2: Cellular Jail\nDay 3: Havelock\nDay 4: Beach and snorkelling\nDay 5: Leisure\nDay 6: Departure', image=IMG.format(id='photo-1544551763-46a013bb70d5')),
    dict(name='Dubai Family Premium', city='Dubai', days=6, price=54999, sale=46999, type='family', tour='private', group='2-6', langs='English, Hindi', featured=True, seats=18, desc='Premium Dubai holiday with desert safari, Burj Khalifa, marina cruise and family attractions.', highlights='Burj Khalifa\nDesert safari\nDubai Marina\nDubai Mall', inc='Hotel, Breakfast, Airport transfers, City tour, Desert safari', exc='Flights, Visa, Attraction upgrades, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Dubai city tour\nDay 3: Burj Khalifa and Mall\nDay 4: Desert safari\nDay 5: Marina and leisure\nDay 6: Departure', image=IMG.format(id='photo-1512453979798-5ea266f8880c')),
    dict(name='Bali Wellness & Beach Escape', city='Bali', days=6, price=49999, sale=41999, type='honeymoon', tour='private', group='2', langs='English, Hindi', featured=True, seats=14, desc='Romantic Bali itinerary with Ubud culture, beach resorts, spa time and sunset experiences.', highlights='Ubud\nBeach resort\nCouples spa\nSunset temple', inc='Hotels, Breakfast, Transfers, Sightseeing, Spa session', exc='Flights, Visa, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Ubud and rice terraces\nDay 3: Spa and leisure\nDay 4: Beach resort\nDay 5: Sunset temple\nDay 6: Departure', image=IMG.format(id='photo-1537996194471-e657df975ab4')),
    dict(name='Maldives Private Island Escape', city='Maldives', days=5, price=89999, sale=74999, type='honeymoon', tour='private', group='2', langs='English, Hindi', featured=True, seats=10, desc='Private-island romantic escape with overwater accommodation, lagoon time and sunset cruises.', highlights='Overwater villa\nLagoon experience\nSunset cruise\nCouples dinner', inc='Resort, Breakfast, Transfers, Sunset cruise, Selected meals', exc='Flights, Insurance, Water sports, Personal expenses', itinerary='Day 1: Arrival and resort\nDay 2: Lagoon and leisure\nDay 3: Sunset cruise\nDay 4: Couples experience\nDay 5: Departure', image=IMG.format(id='photo-1514282401047-d79a71a590e8')),
    dict(name='Singapore Explorer Plus', city='Singapore', days=6, price=59999, sale=50999, type='family', tour='private', group='2-6', langs='English, Hindi', featured=False, seats=16, desc='Extended Singapore family trip with Sentosa, Gardens by the Bay, Universal Studios and Night Safari.', highlights='Gardens by the Bay\nSentosa\nUniversal Studios\nNight Safari', inc='Hotel, Breakfast, Transfers, City tour, Selected attraction tickets', exc='Flights, Visa, Optional upgrades, Personal expenses', itinerary='Day 1: Arrival\nDay 2: City and Gardens by the Bay\nDay 3: Sentosa\nDay 4: Universal Studios\nDay 5: Night Safari\nDay 6: Departure', image=IMG.format(id='photo-1525625293386-3f8f99389edd')),
    dict(name='Paris Swiss Romance', city='Paris', days=8, price=109999, sale=94999, type='honeymoon', tour='private', group='2', langs='English, Hindi', featured=True, seats=8, desc='Romantic Europe combination of Paris highlights and Swiss alpine scenery.', highlights='Eiffel Tower\nSeine cruise\nLucerne\nInterlaken', inc='Hotels, Breakfast, Transfers, Seine cruise, Selected rail tickets', exc='International flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Paris arrival\nDay 2: Eiffel Tower\nDay 3: Louvre and Montmartre\nDay 4: Paris leisure\nDay 5: Travel to Switzerland\nDay 6: Lucerne\nDay 7: Interlaken\nDay 8: Departure', image=IMG.format(id='photo-1502602898657-3e91760cbb34')),
    dict(name='Switzerland Family Alpine Tour', city='Interlaken', days=8, price=99999, sale=87999, type='family', tour='private', group='2-6', langs='English, Hindi', featured=True, seats=10, desc='Family-friendly Swiss journey through Lucerne, Interlaken and mountain viewpoints.', highlights='Lucerne\nJungfraujoch\nLake cruise\nSwiss villages', inc='Hotels, Breakfast, Rail passes, Transfers, Selected excursions', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Zurich arrival\nDay 2: Lucerne\nDay 3: Interlaken\nDay 4: Jungfraujoch\nDay 5: Lake cruise\nDay 6: Swiss village\nDay 7: Leisure\nDay 8: Departure', image=IMG.format(id='photo-1527668752968-14dc70a27c95')),
    dict(name='London Paris Family Circuit', city='London', days=8, price=99999, sale=85999, type='cultural', tour='private', group='2-6', langs='English, Hindi', featured=False, seats=12, desc='Classic family Europe break combining London landmarks with Paris culture and sightseeing.', highlights='Westminster\nTower Bridge\nEiffel Tower\nSeine cruise', inc='Hotels, Breakfast, Transfers, City tours, Selected cruise', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: London arrival\nDay 2: Westminster\nDay 3: Tower Bridge\nDay 4: London leisure\nDay 5: Paris transfer\nDay 6: Eiffel Tower\nDay 7: Louvre and Seine\nDay 8: Departure', image=IMG.format(id='photo-1513635269975-59663e0ac1ad')),
])


# Additional Europe destinations and packages for the expanded catalogue.
EUROPE_DESTINATIONS = [
    ('Rome & Vatican', 'Rome', 'Italy', 'Ancient ruins, Vatican City, Italian food and timeless Roman streets.', 41.9028, 12.4964, 'Apr - Jun, Sep - Oct', True, IMG.format(id='photo-1529260830199-42c24126f198')),
    ('Santorini Escape', 'Santorini', 'Greece', 'Whitewashed villages, Aegean sunsets, caldera views and island relaxation.', 36.3932, 25.4615, 'May - Oct', True, IMG.format(id='photo-1570077188670-e3a8d69ac5ff')),
    ('Swiss Zurich & Lucerne', 'Zurich', 'Switzerland', 'Lakeside cities, alpine rail journeys and scenic Swiss villages.', 47.3769, 8.5417, 'Jun - Sep', False, IMG.format(id='photo-1521292270410-a8c4d716d518')),
    ('Barcelona & Catalonia', 'Barcelona', 'Spain', 'Gaudi architecture, Mediterranean beaches, tapas and Catalonian culture.', 41.3874, 2.1686, 'Apr - Jun, Sep - Oct', True, IMG.format(id='photo-1539037116277-4db20889f2d4')),
    ('Amsterdam Canals', 'Amsterdam', 'Netherlands', 'Canals, museums, cycling culture and charming Dutch neighbourhoods.', 52.3676, 4.9041, 'Apr - Sep', False, IMG.format(id='photo-1534351590666-13e3e96b5017')),
    ('Prague Heritage', 'Prague', 'Czech Republic', 'Fairytale old town, castles, bridges and Central European charm.', 50.0755, 14.4378, 'Apr - Oct', True, IMG.format(id='photo-1541849546-216549ae216d')),
    ('Vienna Imperial', 'Vienna', 'Austria', 'Imperial palaces, classical music, cafes and elegant European avenues.', 48.2082, 16.3738, 'Apr - Oct', False, IMG.format(id='photo-1516550893923-42d28e5677af')),
    ('Budapest Danube', 'Budapest', 'Hungary', 'Danube views, thermal baths, historic architecture and vibrant nightlife.', 47.4979, 19.0402, 'Apr - Oct', False, IMG.format(id='photo-1541849546-216549ae216d')),
    ('Lisbon & Sintra', 'Lisbon', 'Portugal', 'Colourful streets, Atlantic viewpoints, historic trams and Sintra palaces.', 38.7223, -9.1393, 'Mar - Oct', True, IMG.format(id='photo-1555881400-74d7acaacd8b')),
    ('Iceland Aurora', 'Reykjavik', 'Iceland', 'Northern lights, waterfalls, glaciers and dramatic volcanic landscapes.', 64.1466, -21.9426, 'Sep - Mar', True, IMG.format(id='photo-1520769945061-0a448c463865')),
    ('Norway Fjords', 'Bergen', 'Norway', 'Majestic fjords, scenic railways, waterfalls and Nordic coastal landscapes.', 60.3913, 5.3221, 'May - Sep', True, IMG.format(id='photo-1531366936337-7c912a4589a7')),
    ('Croatia Adriatic', 'Dubrovnik', 'Croatia', 'Adriatic coastlines, medieval walls, island cruises and seaside towns.', 42.6507, 18.0944, 'May - Oct', False, '/static/images/croatia-dubrovnik-escape.svg'),
]

EUROPE_PACKAGES = [
    dict(name='Italy Rome & Florence Discovery', city='Rome', days=7, price=109999, sale=94999, type='cultural', tour='private', group='2-8', langs='English, Hindi', featured=True, seats=12, desc='A classic Italy journey through Rome, Vatican City, Florence and Tuscan culture.', highlights='Colosseum\nVatican City\nFlorence Duomo\nTuscan experience', inc='Hotels, Breakfast, Transfers, Guided sightseeing, Selected rail tickets', exc='International flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Rome arrival\nDay 2: Colosseum and Roman Forum\nDay 3: Vatican City\nDay 4: Train to Florence\nDay 5: Florence highlights\nDay 6: Tuscany excursion\nDay 7: Departure', image=IMG.format(id='photo-1529260830199-42c24126f198')),
    dict(name='Rome Family Holiday', city='Rome', days=6, price=89999, sale=77999, type='family', tour='private', group='2-6', langs='English, Hindi', featured=False, seats=14, desc='Family-friendly Rome with ancient landmarks, pizza experiences and relaxed sightseeing.', highlights='Colosseum\nTrevi Fountain\nVatican\nPizza class', inc='Hotel, Breakfast, Transfers, City tour, Activity', exc='Flights, Visa, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Ancient Rome\nDay 3: Vatican\nDay 4: Family food experience\nDay 5: Leisure\nDay 6: Departure', image=IMG.format(id='photo-1529260830199-42c24126f198')),
    dict(name='Santorini Honeymoon Escape', city='Santorini', days=5, price=129999, sale=109999, type='honeymoon', tour='private', group='2', langs='English, Hindi', featured=True, seats=8, desc='Romantic Santorini stay with caldera sunsets, private cruise and island villages.', highlights='Oia sunset\nCaldera cruise\nCave suite\nWine tasting', inc='Premium hotel, Breakfast, Private transfers, Cruise, Wine tasting', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Oia and Fira\nDay 3: Private caldera cruise\nDay 4: Wine and leisure\nDay 5: Departure', image=IMG.format(id='photo-1570077188670-e3a8d69ac5ff')),
    dict(name='Greece Family Island Holiday', city='Santorini', days=7, price=119999, sale=99999, type='family', tour='private', group='2-6', langs='English, Hindi', featured=True, seats=12, desc='Family island holiday with Santorini sightseeing, beach time and Greek cuisine.', highlights='Oia village\nBlack beach\nIsland cruise\nGreek dinner', inc='Hotels, Breakfast, Transfers, Cruise, Sightseeing', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Fira and Oia\nDay 3: Beach day\nDay 4: Cruise\nDay 5: Local villages\nDay 6: Leisure\nDay 7: Departure', image=IMG.format(id='photo-1570077188670-e3a8d69ac5ff')),
    dict(name='Swiss Zurich Lucerne Getaway', city='Zurich', days=6, price=109999, sale=94999, type='family', tour='private', group='2-6', langs='English, Hindi', featured=True, seats=12, desc='Easy-paced Switzerland holiday covering Zurich, Lucerne, lake cruises and alpine scenery.', highlights='Zurich old town\nLucerne lake\nMount Titlis\nSwiss rail journey', inc='Hotels, Breakfast, Rail tickets, Transfers, Selected excursions', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Zurich arrival\nDay 2: Zurich sightseeing\nDay 3: Lucerne\nDay 4: Mount Titlis\nDay 5: Lake experience\nDay 6: Departure', image=IMG.format(id='photo-1521292270410-a8c4d716d518')),
    dict(name='Barcelona Beach & Culture', city='Barcelona', days=6, price=94999, sale=82999, type='cultural', tour='private', group='2-8', langs='English, Hindi', featured=True, seats=16, desc='Barcelona city break blending Gaudi architecture, tapas, beaches and historic quarters.', highlights='Sagrada Familia\nPark Guell\nGothic Quarter\nMediterranean beach', inc='Hotel, Breakfast, Transfers, City tour, Selected entries', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Sagrada Familia and Park Guell\nDay 3: Gothic Quarter\nDay 4: Beach and tapas\nDay 5: Montjuic\nDay 6: Departure', image=IMG.format(id='photo-1539037116277-4db20889f2d4')),
    dict(name='Barcelona Honeymoon Special', city='Barcelona', days=5, price=99999, sale=87999, type='honeymoon', tour='private', group='2', langs='English, Hindi', featured=True, seats=8, desc='Romantic Barcelona escape with boutique stay, sunset views and a private dining experience.', highlights='Gaudi tour\nSunset viewpoint\nCouples dinner\nBeach leisure', inc='Boutique hotel, Breakfast, Transfers, Private experience, Dinner', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Gaudi highlights\nDay 3: Beach and leisure\nDay 4: Sunset and dinner\nDay 5: Departure', image=IMG.format(id='photo-1539037116277-4db20889f2d4')),
    dict(name='Amsterdam Family Explorer', city='Amsterdam', days=5, price=89999, sale=77999, type='family', tour='private', group='2-6', langs='English, Hindi', featured=False, seats=14, desc='Family city break with canal cruise, museums and Dutch countryside.', highlights='Canal cruise\nRijksmuseum\nZaanse Schans\nCycling experience', inc='Hotel, Breakfast, Canal cruise, Transfers, Selected entries', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Canal cruise and old town\nDay 3: Museums\nDay 4: Zaanse Schans\nDay 5: Departure', image=IMG.format(id='photo-1534351590666-13e3e96b5017')),
    dict(name='Prague Romantic Escape', city='Prague', days=5, price=84999, sale=72999, type='honeymoon', tour='private', group='2', langs='English, Hindi', featured=True, seats=8, desc='Romantic Prague with castle views, old town walks, river cruise and Czech dining.', highlights='Prague Castle\nCharles Bridge\nOld Town Square\nVltava cruise', inc='Boutique hotel, Breakfast, Transfers, River cruise, Guided walk', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Old Town\nDay 3: Prague Castle\nDay 4: River cruise and dinner\nDay 5: Departure', image=IMG.format(id='photo-1541849546-216549ae216d')),
    dict(name='Prague Vienna Budapest Circuit', city='Prague', days=9, price=129999, sale=112999, type='cultural', tour='private', group='2-8', langs='English, Hindi', featured=True, seats=12, desc='Central Europe circuit covering Prague, Vienna and Budapest with scenic rail transfers.', highlights='Prague Castle\nVienna Palace\nBudapest Parliament\nDanube cruise', inc='Hotels, Breakfast, Rail transfers, City tours, Cruise', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Prague\nDay 2: Prague highlights\nDay 3: Prague leisure\nDay 4: Vienna transfer\nDay 5: Vienna\nDay 6: Vienna leisure\nDay 7: Budapest transfer\nDay 8: Budapest and Danube\nDay 9: Departure', image=IMG.format(id='photo-1541849546-216549ae216d')),
    dict(name='Vienna Imperial Weekend', city='Vienna', days=4, price=74999, sale=64999, type='cultural', tour='private', group='2-6', langs='English, Hindi', featured=False, seats=16, desc='Elegant Vienna short break featuring palaces, classical culture and coffeehouse traditions.', highlights='Schonbrunn Palace\nHofburg\nClassical concert\nViennese cafe', inc='Hotel, Breakfast, Transfers, Guided tour, Concert ticket', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Schonbrunn and city centre\nDay 3: Hofburg and concert\nDay 4: Departure', image=IMG.format(id='photo-1516550893923-42d28e5677af')),
    dict(name='Budapest Thermal & Danube', city='Budapest', days=5, price=69999, sale=59999, type='cultural', tour='private', group='2-6', langs='English, Hindi', featured=False, seats=16, desc='Budapest city escape with thermal baths, historic sights and evening Danube views.', highlights='Parliament\nThermal baths\nBuda Castle\nDanube cruise', inc='Hotel, Breakfast, Transfers, Bath entry, Cruise', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Buda and Pest\nDay 3: Thermal bath\nDay 4: Danube cruise\nDay 5: Departure', image=IMG.format(id='photo-1541849546-216549ae216d')),
    dict(name='Lisbon & Sintra Discovery', city='Lisbon', days=6, price=79999, sale=69999, type='cultural', tour='private', group='2-8', langs='English, Hindi', featured=True, seats=16, desc='Colourful Lisbon city break with Sintra palaces, coastal views and Portuguese cuisine.', highlights='Tram 28\nBelem\nSintra Palace\nFado evening', inc='Hotel, Breakfast, Transfers, Sintra tour, Fado experience', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Lisbon old town\nDay 3: Belem\nDay 4: Sintra\nDay 5: Fado and leisure\nDay 6: Departure', image=IMG.format(id='photo-1555881400-74d7acaacd8b')),
    dict(name='Portugal Honeymoon Escape', city='Lisbon', days=7, price=109999, sale=94999, type='honeymoon', tour='private', group='2', langs='English, Hindi', featured=True, seats=8, desc='Romantic Portugal holiday with Lisbon, Sintra, ocean viewpoints and private dining.', highlights='Sintra\nOcean viewpoint\nPrivate dinner\nHistoric tram', inc='Boutique hotels, Breakfast, Transfers, Private dinner, Guided tour', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Lisbon\nDay 3: Sintra\nDay 4: Coastline\nDay 5: Leisure\nDay 6: Private dinner\nDay 7: Departure', image=IMG.format(id='photo-1555881400-74d7acaacd8b')),
    dict(name='Iceland Northern Lights', city='Reykjavik', days=6, price=149999, sale=129999, type='adventure', tour='group', group='4-12', langs='English', featured=True, seats=12, desc='Winter Iceland adventure with Northern Lights, waterfalls, geothermal landscapes and the Golden Circle.', highlights='Northern Lights\nGolden Circle\nWaterfalls\nBlue Lagoon', inc='Hotels, Breakfast, Guided tours, Transfers, Lagoon entry', exc='Flights, Insurance, Personal expenses', itinerary='Day 1: Reykjavik\nDay 2: Golden Circle\nDay 3: South Coast\nDay 4: Northern Lights hunt\nDay 5: Blue Lagoon\nDay 6: Departure', image=IMG.format(id='photo-1520769945061-0a448c463865')),
    dict(name='Norway Fjords Adventure', city='Bergen', days=7, price=159999, sale=139999, type='adventure', tour='group', group='4-12', langs='English', featured=True, seats=12, desc='Scenic Norway journey through Bergen, fjords, waterfalls and panoramic rail routes.', highlights='Bergen\nFjord cruise\nFlam railway\nWaterfalls', inc='Hotels, Breakfast, Rail tickets, Fjord cruise, Transfers', exc='Flights, Insurance, Personal expenses', itinerary='Day 1: Bergen\nDay 2: Bergen sightseeing\nDay 3: Fjord cruise\nDay 4: Flam railway\nDay 5: Fjord village\nDay 6: Leisure\nDay 7: Departure', image=IMG.format(id='photo-1531366936337-7c912a4589a7')),
    dict(name='Norway Honeymoon Fjords', city='Bergen', days=8, price=179999, sale=154999, type='honeymoon', tour='private', group='2', langs='English', featured=True, seats=6, desc='A romantic Nordic escape with fjord cruises, boutique stays and scenic rail journeys.', highlights='Private fjord cruise\nFjord hotel\nFlam railway\nSunset views', inc='Boutique hotels, Breakfast, Private transfers, Cruise, Rail tickets', exc='Flights, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Bergen\nDay 3: Fjord cruise\nDay 4: Scenic railway\nDay 5: Fjord village\nDay 6: Leisure\nDay 7: Romantic cruise\nDay 8: Departure', image=IMG.format(id='photo-1531366936337-7c912a4589a7')),
    dict(name='Croatia Dubrovnik Escape', city='Dubrovnik', days=6, price=89999, sale=77999, type='beach', tour='private', group='2-6', langs='English, Hindi', featured=False, seats=14, desc='Adriatic holiday with Dubrovnik old town, island cruising and coastal relaxation.', highlights='Old City walls\nAdriatic cruise\nIsland visit\nBeach day', inc='Hotel, Breakfast, Transfers, Cruise, City tour', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Old Town\nDay 3: Island cruise\nDay 4: Beach leisure\nDay 5: Coastal drive\nDay 6: Departure', image=IMG.format(id='photo-1555993539-1732b0258235')),
    dict(name='Croatia Honeymoon Adriatic', city='Dubrovnik', days=7, price=109999, sale=94999, type='honeymoon', tour='private', group='2', langs='English', featured=True, seats=8, desc='Romantic Dubrovnik experience with sea-view accommodation, island cruise and private dinner.', highlights='Sea-view stay\nIsland cruise\nOld Town sunset\nPrivate dinner', inc='Hotel, Breakfast, Transfers, Cruise, Dinner', exc='Flights, Visa, Insurance, Personal expenses', itinerary='Day 1: Arrival\nDay 2: Old Town\nDay 3: Island cruise\nDay 4: Beach\nDay 5: Private dinner\nDay 6: Leisure\nDay 7: Departure', image=IMG.format(id='photo-1555993539-1732b0258235')),
]

# A curated travel-image pool used to give every package its own 5-image gallery.
# The first image remains the package cover; the next four are unique supporting views.
GALLERY_POOL = [
    'photo-1469474968028-56623f02e42e',
    'photo-1500534623283-312aade485b7',
    'photo-1470770841072-f978cf4d019e',
    'photo-1500530855697-b586d89ba3ee',
    'photo-1501785888041-af3ef285b470',
    'photo-1441974231531-c6227db76b6e',
    'photo-1507525428034-b723cf961d3e',
    'photo-1506744038136-46273834b3fb',
    'photo-1511497584788-876760111969',
    'photo-1501854140801-50d01698950b',
    'photo-1519817650390-64a93db51149',
    'photo-1519681393784-d120267933ba',
    'photo-1470214304380-aadaedcfff1b',
    'photo-1516483638261-f4dbaf036963',
    'photo-1523906834658-6e24ef2386f9',
    'photo-1533105079780-92b9be482077',
    'photo-1505761671935-60b3a7427bad',
    'photo-1499856871958-5b9627545d1a',
    'photo-1494526585095-c41746248156',
    'photo-1533929736458-ca588d08c8be',
    'photo-1530789253388-582c481c54b0',
    'photo-1518391846015-55a9cc003b25',
    'photo-1526778548025-fa2f459cd5c1',
    'photo-1528127269322-539801943592',
    'photo-1523480717984-24cba35ae1ef',
    'photo-1529107386315-e1a2ed48a620',
    'photo-1521292270410-a8c4d716d518',
    'photo-1527631746610-bca00a040d60',
    'photo-1513415277900-a62401e19be4',
    'photo-1518684079-3c830dcef090',
    'photo-1512453979798-5ea266f8880c',
    'photo-1537996194471-e657df975ab4',
    'photo-1514282401047-d79a71a590e8',
    'photo-1540202404-a2f29016b523',
    'photo-1502602898657-3e91760cbb34',
    'photo-1527668752968-14dc70a27c95',
    'photo-1513635269975-59663e0ac1ad',
    'photo-1544735716-392fe2489ffa',
    'photo-1605649487212-47bdab064df7',
    'photo-1602216056096-3b40cc0c9944',
    'photo-1599661046289-e31897846e41',
    'photo-1564507592333-c60657eea523',
]

CITY_POOLS = {'Goa': ['photo-1512343879784-a960bf40e7f2',
         'photo-1507525428034-b723cf961d3e',
         'photo-1533105079780-92b9be482077',
         'photo-1500530855697-b586d89ba3ee',
         'photo-1470770841072-f978cf4d019e',
         'photo-1506744038136-46273834b3fb',
         'photo-1511497584788-876760111969',
         'photo-1501785888041-af3ef285b470'],
 'Manali': ['photo-1506905925346-21bda4d32df4',
            'photo-1476514525535-07fb3b4ae5f1',
            'photo-1501785888041-af3ef285b470',
            'photo-1519681393784-d120267933ba',
            'photo-1470214304380-aadaedcfff1b',
            'photo-1469474968028-56623f02e42e',
            'photo-1500530855697-b586d89ba3ee',
            'photo-1506744038136-46273834b3fb'],
 'Alleppey': ['photo-1602216056096-3b40cc0c9944',
              'photo-1593693411515-c20261bcad6e',
              'photo-1506744038136-46273834b3fb',
              'photo-1511497584788-876760111969',
              'photo-1501854140801-50d01698950b',
              'photo-1470770841072-f978cf4d019e',
              'photo-1500530855697-b586d89ba3ee',
              'photo-1469474968028-56623f02e42e'],
 'Jaipur': ['photo-1599661046289-e31897846e41',
            'photo-1519817650390-64a93db51149',
            'photo-1523906834658-6e24ef2386f9',
            'photo-1523480717984-24cba35ae1ef',
            'photo-1529107386315-e1a2ed48a620',
            'photo-1521292270410-a8c4d716d518',
            'photo-1499856871958-5b9627545d1a',
            'photo-1533929736458-ca588d08c8be'],
 'Agra': ['photo-1564507592333-c60657eea523',
          'photo-1599661046289-e31897846e41',
          'photo-1519817650390-64a93db51149',
          'photo-1523906834658-6e24ef2386f9',
          'photo-1523480717984-24cba35ae1ef',
          'photo-1499856871958-5b9627545d1a',
          'photo-1533929736458-ca588d08c8be',
          'photo-1500530855697-b586d89ba3ee'],
 'Srinagar': ['photo-1605649487212-47bdab064df7',
              'photo-1582972236019-ea9f0c9a8c1f',
              'photo-1501785888041-af3ef285b470',
              'photo-1519681393784-d120267933ba',
              'photo-1470770841072-f978cf4d019e',
              'photo-1469474968028-56623f02e42e',
              'photo-1506744038136-46273834b3fb',
              'photo-1501854140801-50d01698950b'],
 'Leh': ['photo-1544735716-392fe2489ffa',
         'photo-1548013146-72479768bada',
         'photo-1519681393784-d120267933ba',
         'photo-1470214304380-aadaedcfff1b',
         'photo-1501785888041-af3ef285b470',
         'photo-1469474968028-56623f02e42e',
         'photo-1506744038136-46273834b3fb',
         'photo-1528127269322-539801943592'],
 'Mysuru': ['photo-1601050690597-df0568f70950',
            'photo-1519817650390-64a93db51149',
            'photo-1523906834658-6e24ef2386f9',
            'photo-1523480717984-24cba35ae1ef',
            'photo-1529107386315-e1a2ed48a620',
            'photo-1521292270410-a8c4d716d518',
            'photo-1533929736458-ca588d08c8be',
            'photo-1499856871958-5b9627545d1a'],
 'Mysore': ['photo-1590050752117-23a9d2c8a4d3',
            'photo-1519817650390-64a93db51149',
            'photo-1523906834658-6e24ef2386f9',
            'photo-1523480717984-24cba35ae1ef',
            'photo-1529107386315-e1a2ed48a620',
            'photo-1521292270410-a8c4d716d518',
            'photo-1533929736458-ca588d08c8be',
            'photo-1499856871958-5b9627545d1a'],
 'Kodaikanal': ['photo-1582610116397-edb318620f90',
                'photo-1500534623283-312aade485b7',
                'photo-1501785888041-af3ef285b470',
                'photo-1470770841072-f978cf4d019e',
                'photo-1506744038136-46273834b3fb',
                'photo-1519681393784-d120267933ba',
                'photo-1469474968028-56623f02e42e',
                'photo-1501854140801-50d01698950b'],
 'Ooty': ['photo-1597074866923-dc0589150358',
          'photo-1500534623283-312aade485b7',
          'photo-1501785888041-af3ef285b470',
          'photo-1470770841072-f978cf4d019e',
          'photo-1506744038136-46273834b3fb',
          'photo-1519681393784-d120267933ba',
          'photo-1469474968028-56623f02e42e',
          'photo-1501854140801-50d01698950b'],
 'Port Blair': ['photo-1540202404-a2f29016b523',
                'photo-1544551763-46a013bb70d5',
                'photo-1507525428034-b723cf961d3e',
                'photo-1514282401047-d79a71a590e8',
                'photo-1533105079780-92b9be482077',
                'photo-1506744038136-46273834b3fb',
                'photo-1511497584788-876760111969',
                'photo-1470770841072-f978cf4d019e'],
 'Dubai': ['photo-1512453979798-5ea266f8880c',
           'photo-1518684079-3c830dcef090',
           'photo-1527631746610-bca00a040d60',
           'photo-1533929736458-ca588d08c8be',
           'photo-1501854140801-50d01698950b',
           'photo-1494526585095-c41746248156',
           'photo-1519817650390-64a93db51149',
           'photo-1521292270410-a8c4d716d518'],
 'Denpasar': ['photo-1537996194471-e657df975ab4',
              'photo-1539367628448-4bc5c9d171c8',
              'photo-1507525428034-b723cf961d3e',
              'photo-1514282401047-d79a71a590e8',
              'photo-1500530855697-b586d89ba3ee',
              'photo-1506744038136-46273834b3fb',
              'photo-1511497584788-876760111969',
              'photo-1470770841072-f978cf4d019e'],
 'Bali': ['photo-1537996194471-e657df975ab4',
          'photo-1539367628448-4bc5c9d171c8',
          'photo-1507525428034-b723cf961d3e',
          'photo-1514282401047-d79a71a590e8',
          'photo-1500530855697-b586d89ba3ee',
          'photo-1506744038136-46273834b3fb',
          'photo-1511497584788-876760111969',
          'photo-1470770841072-f978cf4d019e'],
 'Malé': ['photo-1514282401047-d79a71a590e8',
          'photo-1507525428034-b723cf961d3e',
          'photo-1533105079780-92b9be482077',
          'photo-1506744038136-46273834b3fb',
          'photo-1511497584788-876760111969',
          'photo-1470770841072-f978cf4d019e',
          'photo-1500530855697-b586d89ba3ee',
          'photo-1537996194471-e657df975ab4'],
 'Maldives': ['photo-1514282401047-d79a71a590e8',
              'photo-1507525428034-b723cf961d3e',
              'photo-1533105079780-92b9be482077',
              'photo-1506744038136-46273834b3fb',
              'photo-1511497584788-876760111969',
              'photo-1470770841072-f978cf4d019e',
              'photo-1500530855697-b586d89ba3ee',
              'photo-1537996194471-e657df975ab4'],
 'Singapore': ['photo-1525625293386-3f8f99389edd',
               'photo-1533929736458-ca588d08c8be',
               'photo-1512453979798-5ea266f8880c',
               'photo-1527631746610-bca00a040d60',
               'photo-1501854140801-50d01698950b',
               'photo-1494526585095-c41746248156',
               'photo-1521292270410-a8c4d716d518',
               'photo-1519817650390-64a93db51149'],
 'Paris': ['photo-1502602898657-3e91760cbb34',
           'photo-1499856871958-5b9627545d1a',
           'photo-1526778548025-fa2f459cd5c1',
           'photo-1523906834658-6e24ef2386f9',
           'photo-1516483638261-f4dbaf036963',
           'photo-1523480717984-24cba35ae1ef',
           'photo-1529107386315-e1a2ed48a620',
           'photo-1533929736458-ca588d08c8be'],
 'Interlaken': ['photo-1527668752968-14dc70a27c95',
                'photo-1501785888041-af3ef285b470',
                'photo-1519681393784-d120267933ba',
                'photo-1470770841072-f978cf4d019e',
                'photo-1469474968028-56623f02e42e',
                'photo-1506744038136-46273834b3fb',
                'photo-1528127269322-539801943592',
                'photo-1516483638261-f4dbaf036963'],
 'London': ['photo-1513635269975-59663e0ac1ad',
            'photo-1529107386315-e1a2ed48a620',
            'photo-1533929736458-ca588d08c8be',
            'photo-1521292270410-a8c4d716d518',
            'photo-1499856871958-5b9627545d1a',
            'photo-1523906834658-6e24ef2386f9',
            'photo-1516483638261-f4dbaf036963',
            'photo-1526778548025-fa2f459cd5c1'],
 'Rome': ['photo-1529260830199-42c24126f198',
          'photo-1499856871958-5b9627545d1a',
          'photo-1523906834658-6e24ef2386f9',
          'photo-1516483638261-f4dbaf036963',
          'photo-1523480717984-24cba35ae1ef',
          'photo-1529107386315-e1a2ed48a620',
          'photo-1533929736458-ca588d08c8be',
          'photo-1521292270410-a8c4d716d518'],
 'Santorini': ['photo-1570077188670-e3a8d69ac5ff',
               'photo-1533105079780-92b9be482077',
               'photo-1507525428034-b723cf961d3e',
               'photo-1500530855697-b586d89ba3ee',
               'photo-1514282401047-d79a71a590e8',
               'photo-1470770841072-f978cf4d019e',
               'photo-1506744038136-46273834b3fb',
               'photo-1511497584788-876760111969'],
 'Zurich': ['photo-1521292270410-a8c4d716d518',
            'photo-1527668752968-14dc70a27c95',
            'photo-1501785888041-af3ef285b470',
            'photo-1519681393784-d120267933ba',
            'photo-1469474968028-56623f02e42e',
            'photo-1506744038136-46273834b3fb',
            'photo-1516483638261-f4dbaf036963',
            'photo-1528127269322-539801943592'],
 'Barcelona': ['photo-1539037116277-4db20889f2d4',
               'photo-1523480717984-24cba35ae1ef',
               'photo-1523906834658-6e24ef2386f9',
               'photo-1499856871958-5b9627545d1a',
               'photo-1516483638261-f4dbaf036963',
               'photo-1529107386315-e1a2ed48a620',
               'photo-1533929736458-ca588d08c8be',
               'photo-1521292270410-a8c4d716d518'],
 'Amsterdam': ['photo-1534351590666-13e3e96b5017',
               'photo-1521292270410-a8c4d716d518',
               'photo-1529107386315-e1a2ed48a620',
               'photo-1533929736458-ca588d08c8be',
               'photo-1499856871958-5b9627545d1a',
               'photo-1523906834658-6e24ef2386f9',
               'photo-1516483638261-f4dbaf036963',
               'photo-1523480717984-24cba35ae1ef'],
 'Prague': ['photo-1541849546-216549ae216d',
            'photo-1521292270410-a8c4d716d518',
            'photo-1529107386315-e1a2ed48a620',
            'photo-1533929736458-ca588d08c8be',
            'photo-1499856871958-5b9627545d1a',
            'photo-1523906834658-6e24ef2386f9',
            'photo-1516483638261-f4dbaf036963',
            'photo-1523480717984-24cba35ae1ef'],
 'Vienna': ['photo-1516550893923-42d28e5677af',
            'photo-1521292270410-a8c4d716d518',
            'photo-1529107386315-e1a2ed48a620',
            'photo-1533929736458-ca588d08c8be',
            'photo-1499856871958-5b9627545d1a',
            'photo-1523906834658-6e24ef2386f9',
            'photo-1516483638261-f4dbaf036963',
            'photo-1523480717984-24cba35ae1ef'],
 'Budapest': ['photo-1541849546-216549ae216d',
              'photo-1521292270410-a8c4d716d518',
              'photo-1529107386315-e1a2ed48a620',
              'photo-1533929736458-ca588d08c8be',
              'photo-1499856871958-5b9627545d1a',
              'photo-1523906834658-6e24ef2386f9',
              'photo-1516483638261-f4dbaf036963',
              'photo-1523480717984-24cba35ae1ef'],
 'Lisbon': ['photo-1555881400-74d7acaacd8b',
            'photo-1521292270410-a8c4d716d518',
            'photo-1529107386315-e1a2ed48a620',
            'photo-1533929736458-ca588d08c8be',
            'photo-1499856871958-5b9627545d1a',
            'photo-1523906834658-6e24ef2386f9',
            'photo-1516483638261-f4dbaf036963',
            'photo-1523480717984-24cba35ae1ef'],
 'Reykjavik': ['photo-1520769945061-0a448c463865',
               'photo-1501785888041-af3ef285b470',
               'photo-1519681393784-d120267933ba',
               'photo-1469474968028-56623f02e42e',
               'photo-1470770841072-f978cf4d019e',
               'photo-1506744038136-46273834b3fb',
               'photo-1528127269322-539801943592',
               'photo-1516483638261-f4dbaf036963'],
 'Bergen': ['photo-1531366936337-7c912a4589a7',
            'photo-1528127269322-539801943592',
            'photo-1501785888041-af3ef285b470',
            'photo-1519681393784-d120267933ba',
            'photo-1469474968028-56623f02e42e',
            'photo-1470770841072-f978cf4d019e',
            'photo-1506744038136-46273834b3fb',
            'photo-1516483638261-f4dbaf036963'],
 'Dubrovnik': ['photo-1555993539-1732b0258235',
               'photo-1528127269322-539801943592',
               'photo-1533105079780-92b9be482077',
               'photo-1507525428034-b723cf961d3e',
               'photo-1516483638261-f4dbaf036963',
               'photo-1523906834658-6e24ef2386f9',
               'photo-1506744038136-46273834b3fb',
               'photo-1533929736458-ca588d08c8be']}

def unsplash(photo_id):
    return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w=1400&q=88"

def package_cover_url(package_name, city, package_type, source_image=''):
    """Use the catalogue's package image as the cover whenever available."""
    if source_image and source_image.startswith('photo-'):
        return unsplash(source_image)
    # Croatia and any future package without an Unsplash source image.
    pool = CITY_POOLS.get(city, CITY_POOLS["Paris"])
    return unsplash(pool[0])


def package_image_query(package_name, city, package_type, slot=0, source_image=''):
    """Return a real destination-specific image for this exact package/slot."""
    pool = CITY_POOLS.get(city, CITY_POOLS["Paris"])
    cover = source_image if source_image.startswith('photo-') else None

    # Deterministic rotation makes different packages in the same destination
    # receive different combinations instead of one repeated gallery.
    seed_value = int(md5(f"{package_name}|{city}|{package_type}".encode("utf-8")).hexdigest()[:8], 16)
    ordered = pool[seed_value % len(pool):] + pool[:seed_value % len(pool)]

    if cover:
        ordered = [cover] + [x for x in ordered if x != cover]

    pid = ordered[slot % len(ordered)]
    return unsplash(pid)


def gallery(package_name, city, package_type, source_image=''):
    """Five real images, selected from the package's destination pool."""
    pool = CITY_POOLS.get(city, CITY_POOLS["Paris"])
    seed_value = int(md5(f"{package_name}|{city}|{package_type}".encode("utf-8")).hexdigest()[:8], 16)
    ordered = pool[seed_value % len(pool):] + pool[:seed_value % len(pool)]

    if source_image.startswith('photo-'):
        ordered = [source_image] + [x for x in ordered if x != source_image]

    # Guarantee five different image URLs inside every package gallery.
    selected = ordered[:5]
    return '\n'.join(unsplash(pid) for pid in selected)


# Package-specific hotel names shown in the Included section.
# These are catalogue/demo selections; replace them in Admin when a confirmed property is chosen.
HOTELS = {
    'Goa': 'Hotel: Taj Cidade de Goa Horizon',
    'Manali': 'Hotel: The Himalayan',
    'Alleppey': 'Hotel: Ramada by Wyndham Alleppey',
    'Jaipur': 'Hotel: ITC Rajputana',
    'Agra': 'Hotel: ITC Mughal',
    'Srinagar': 'Hotel: The Lalit Grand Palace Srinagar',
    'Leh': 'Hotel: The Grand Dragon Ladakh',
    'Mysuru': 'Hotel: Radisson Blu Plaza Hotel Mysore',
    'Mysore': 'Hotel: Radisson Blu Plaza Hotel Mysore',
    'Kodaikanal': 'Hotel: The Carlton Kodaikanal',
    'Ooty': 'Hotel: Sterling Ooty Elk Hill',
    'Port Blair': 'Hotel: Welcomhotel by ITC Hotels - Bay Island',
    'Dubai': 'Hotel: Novotel Dubai Al Barsha',
    'Denpasar': 'Hotel: Anantara Seminyak Bali Resort',
    'Bali': 'Hotel: Anantara Seminyak Bali Resort',
    'Malé': 'Resort: Kurumba Maldives',
    'Maldives': 'Resort: Kurumba Maldives',
    'Singapore': 'Hotel: PARKROYAL COLLECTION Marina Bay',
    'Paris': 'Hotel: Novotel Paris Centre Tour Eiffel',
    'Interlaken': 'Hotel: Hotel Interlaken',
    'London': 'Hotel: Novotel London Blackfriars',
    'Rome': 'Hotel: NH Collection Roma Centro',
    'Barcelona': 'Hotel: H10 Metropolitan Barcelona',
    'Amsterdam': 'Hotel: Park Plaza Victoria Amsterdam',
    'Prague': 'Hotel: NH Collection Prague Carlo IV',
    'Vienna': 'Hotel: Austria Trend Hotel Europa Wien',
    'Budapest': 'Hotel: Danubius Hotel Astoria City Center',
    'Lisbon': 'Hotel: HF Fenix Lisboa',
    'Reykjavik': 'Hotel: Fosshotel Reykjavik',
    'Bergen': 'Hotel: Scandic Torget Bergen',
    'Dubrovnik': 'Hotel: Valamar Lacroma Dubrovnik Hotel',
    'Santorini': 'Hotel: El Greco Resort & Spa',
    'Zurich': 'Hotel: Hotel St. Gotthard Zürich',
}

def detailed_inclusions(raw, city):
    """Normalize the catalogue into clear customer-facing inclusions."""
    parts = [x.strip() for x in raw.split(',') if x.strip()]
    result = []
    hotel = HOTELS.get(city, f'Hotel: Selected 4-star property in {city}')
    result.append(hotel)
    result.append('Breakfast: Daily breakfast on all accommodation days')
    result.append('Visa: Visa assistance included')

    # Remove vague/duplicate transport, meal and ticket labels; add clear versions below.
    for part in parts:
        low = part.lower()
        if low.startswith(('hotel', 'hotels', 'resort', '5-star', '4-star', 'premium villa', 'boutique hotel', 'boutique hotels')):
            continue
        if 'breakfast' in low:
            continue
        if 'visa' in low:
            continue
        if any(word in low for word in ('airport transfer', 'transfers', 'transfer', 'private vehicle', 'private cab', 'private car', 'support vehicle')):
            continue
        if any(word in low for word in ('rail pass', 'rail ticket', 'train ticket')):
            continue
        if any(word in low for word in ('sightseeing', 'city tour', 'selected entries', 'selected attraction tickets')):
            continue
        if 'selected meals' in low:
            continue
        if low in {'driver'}:
            continue
        if 'dinner' in low:
            # e.g. "Dinner" / "Candlelight dinner" / "Private beach dinner"
            result.append(f"{part}: Veg & Non-Veg options available on all accommodation days")
            continue
        result.append(part)

    result.append('Train tickets: Included for scheduled train journeys where listed in the itinerary')
    result.append('Local sightseeing tickets: Entry tickets for the listed local sightseeing')
    result.append('Transport: AC / Non-AC car / bus / van based on the group size and itinerary')
    if not any('excursion' in x.lower() for x in result):
        result.append('Selected excursions: Experiences specifically listed in the itinerary')
    result.append('Travel insurance')
    return ', '.join(dict.fromkeys(result))


def build_itinerary_days(item, city):
    """Turn a package's 'Day N: Title' itinerary lines into structured,
    package-specific ItineraryDay rows instead of one generic description
    repeated for every day of every package.

    Uses that package's own highlights/inclusions/tour type so two packages
    with similar day counts still read differently. Admins can edit or
    rewrite any of this afterwards in Django Admin.
    """
    lines = [l.strip() for l in item['itinerary'].splitlines() if l.strip()]
    highlights = [h.strip() for h in item.get('highlights', '').splitlines() if h.strip()]
    inc_lower = item.get('inc', '').lower()
    if 'all meals' in inc_lower:
        default_meal = 'BLD'
    elif 'breakfast' in inc_lower:
        default_meal = 'B'
    else:
        default_meal = ''

    tour_label = {'private': 'Private', 'group': 'Group', 'daily': 'Daily', 'custom': 'Custom'}.get(item.get('tour', ''), 'Guided')
    total = len(lines)
    highlight_idx = 0
    days = []

    for idx, line in enumerate(lines, start=1):
        title = line.split(':', 1)[1].strip() if ':' in line else line
        is_arrival = idx == 1
        is_departure = idx == total and total > 1

        highlight = None
        if highlights and not is_departure:
            highlight = highlights[highlight_idx % len(highlights)]
            highlight_idx += 1

        sentences = []
        if is_arrival:
            sentences.append(f"Arrive in {city} and check in to your stay; the rest of the day is kept relaxed to settle in.")
            if highlight:
                sentences.append(f"If time allows after arrival, there's a first look at {highlight.lower()}.")
        elif is_departure:
            sentences.append(f"Enjoy breakfast at leisure before checking out and transferring for departure from {city}, wrapping up the trip.")
        else:
            if highlight:
                sentences.append(f"Today centres on {highlight}, with unhurried time built in to properly experience it.")
            else:
                sentences.append(f"A full day exploring {title.lower()}, paced around your group's preferences.")
            sentences.append(f"{tour_label} transport and local support are arranged for the day, in line with what's included in this package.")

        activities = [highlight] if (highlight and not is_arrival and not is_departure) else []
        meals = 'B' if (is_departure and default_meal) else default_meal
        overnight = '' if is_departure else f"Overnight in {city}"

        days.append(dict(
            day_number=idx,
            title=title,
            description=' '.join(sentences),
            activities='\n'.join(activities),
            meals=meals,
            overnight_stay=overnight,
        ))
    return days


def detailed_exclusions(raw):
    """Normalize the exclusions list: drop Visa (now shown as included),
    and rename Flights -> Flight tickets for clearer customer-facing copy."""
    result = []
    for part in raw.split(','):
        part = part.strip()
        low = part.lower()
        if not part:
            continue
        if low in {'insurance', 'travel insurance'}:
            continue
        if 'visa' in low:
            continue
        if low == 'flights':
            result.append('Flight tickets')
            continue
        if low == 'international flights':
            result.append('International flight tickets')
            continue
        result.append(part)
    return ', '.join(dict.fromkeys(result))


class Command(BaseCommand):
    help = 'Create/update a rich demo catalogue of destinations and holiday packages.'

    def handle(self, *args, **options):
        destinations = {}
        all_destinations = DESTINATIONS + EUROPE_DESTINATIONS
        for name, city, country, description, lat, lon, best_time, featured, image_url in all_destinations:
            obj, _ = Destination.objects.update_or_create(
                name=name,
                defaults={
                    'city': city, 'country': country, 'description': description,
                    'latitude': lat, 'longitude': lon, 'best_time_to_visit': best_time,
                    'is_featured': featured,
                    'image_url': image_url,
                    'gallery_urls': '\n'.join(DESTINATION_GALLERIES.get(city, [image_url])[:5]),
                },
            )
            destinations[city] = obj

        for item in PACKAGES + EUROPE_PACKAGES:
            destination = destinations.get(item['city']) or Destination.objects.filter(city=item['city']).first()
            if not destination:
                continue
            included = detailed_inclusions(item['inc'], item['city'])
            exclusions = detailed_exclusions(item['exc'])
            package_obj, _ = TravelPackage.objects.update_or_create(
                name=item['name'],
                defaults={
                    'destination': destination,
                    'description': item['desc'],
                    'duration_days': item['days'],
                    'price': item['price'],
                    'discount_price': item['sale'],
                    'package_type': item['type'],
                    'tour_type': item['tour'],
                    'group_size': item['group'],
                    'languages': item['langs'],
                    'highlights': item['highlights'],
                    'inclusions': included,
                    'exclusions': exclusions,
                    'itinerary': item['itinerary'],
                    # Every package gets its own destination/theme image search.
                    # This prevents all packages in the catalogue from sharing the same cover.
                    'image_url': package_cover_url(item['name'], item['city'], item['type'], item.get('image', '')),
                    'gallery_urls': gallery(item['name'], item['city'], item['type'], item.get('image', '')),
                    'travel_guide': f"Plan your {destination.name} journey around the listed itinerary and leave time for local experiences. The best time to visit is {destination.best_time_to_visit or 'season-dependent'}. Carry your documents, comfortable clothing and practical day-trip essentials.",
                    'faqs': 'Is travel insurance included? | Yes. Travel insurance is included in this package.\nCan I customise this journey? | Yes. Contact our travel team to discuss your preferred dates and experiences.\nCan I book for family or friends? | Yes. The booking flow supports multiple travellers.',
                    'insurance_included': True,
                    'is_featured': item['featured'],
                    'available_seats': item['seats'],
                },
            )

            # Replace this package's itinerary days with freshly generated,
            # package-specific ones (admins can hand-edit any of these
            # afterwards in Admin -> Travel Packages -> Itinerary days).
            package_obj.itinerary_days.all().delete()
            ItineraryDay.objects.bulk_create([
                ItineraryDay(package=package_obj, **day)
                for day in build_itinerary_days(item, item['city'])
            ])

        self.stdout.write(self.style.SUCCESS(
            f'Catalogue ready: {Destination.objects.count()} destinations and {TravelPackage.objects.count()} packages.'
        ))
