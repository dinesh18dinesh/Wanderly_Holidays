from django.db import migrations, models


def add_insurance_to_existing_packages(apps, schema_editor):
    TravelPackage = apps.get_model('destinations', 'TravelPackage')
    for package in TravelPackage.objects.all():
        exclusions = package.exclusions or ''
        cleaned = [x.strip() for x in exclusions.split(',') if x.strip()]
        cleaned = [x for x in cleaned if x.lower() not in {'travel insurance', 'insurance'}]
        package.exclusions = ', '.join(cleaned)
        package.insurance_included = True
        package.save(update_fields=['exclusions', 'insurance_included'])


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='gallery_urls',
            field=models.TextField(blank=True, help_text='Optional image URLs, one per line, for the destination gallery.'),
        ),
        migrations.AddField(
            model_name='destination',
            name='highlights',
            field=models.TextField(blank=True, help_text='One destination highlight per line'),
        ),
        migrations.AddField(
            model_name='destination',
            name='things_to_do',
            field=models.TextField(blank=True, help_text='One experience/activity per line'),
        ),
        migrations.AddField(
            model_name='destination',
            name='travel_guide',
            field=models.TextField(blank=True, help_text='Practical travel guide information'),
        ),
        migrations.AddField(
            model_name='travelpackage',
            name='faqs',
            field=models.TextField(blank=True, help_text='One FAQ per line. Format: Question | Answer'),
        ),
        migrations.AddField(
            model_name='travelpackage',
            name='insurance_included',
            field=models.BooleanField(default=True, help_text='Show travel insurance as included in this package.'),
        ),
        migrations.AddField(
            model_name='travelpackage',
            name='travel_guide',
            field=models.TextField(blank=True, help_text='Package-specific travel guide'),
        ),
        migrations.RunPython(add_insurance_to_existing_packages, migrations.RunPython.noop),
    ]
