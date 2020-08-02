# Generated by Django 3.0.7 on 2020-06-14 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='couple_grade',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Couple Grade'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='distance_to_bus_stop',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Distance to Bus Stop'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='distance_to_essential_places',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Distance to Essential Establishments'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='distance_to_subway',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Distance to Subway'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='favorite',
            field=models.BooleanField(default=False, verbose_name='Favorito'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='num_bathrooms',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Number of Bathrooms'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='num_rooms',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Number of Rooms'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='apartment_photos', verbose_name='Picture'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Preço'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='system_grade',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='System Grade'),
        ),
    ]