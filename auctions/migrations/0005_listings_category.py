# Generated by Django 5.0.1 on 2024-04-13 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='category',
            field=models.CharField(default=1, max_length=12),
            preserve_default=False,
        ),
    ]
