# Generated by Django 5.0.1 on 2024-04-13 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listings_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='img_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
