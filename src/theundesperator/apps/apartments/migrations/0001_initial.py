# Generated by Django 3.0.7 on 2020-06-10 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='Address')),
                ('num_rooms', models.CharField(blank=True, max_length=250, null=True, verbose_name='Number of Rooms')),
                ('num_bathrooms', models.CharField(blank=True, max_length=250, null=True, verbose_name='Number of Bathrooms')),
                ('distance_to_subway', models.CharField(blank=True, max_length=250, null=True, verbose_name='Distance to Subway')),
                ('distance_to_bus_stop', models.CharField(blank=True, max_length=250, null=True, verbose_name='Distance to Bus Stop')),
                ('distance_to_essential_places', models.CharField(blank=True, max_length=250, null=True, verbose_name='Distance to Essential Establishments')),
                ('price', models.CharField(blank=True, max_length=250, null=True, verbose_name='Preço')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('couple_grade', models.CharField(blank=True, max_length=250, null=True, verbose_name='Couple Grade')),
                ('system_grade', models.CharField(blank=True, max_length=250, null=True, verbose_name='System Grade')),
                ('picture', models.CharField(blank=True, max_length=250, null=True, verbose_name='Picture')),
                ('contact', models.CharField(blank=True, max_length=250, null=True, verbose_name='Contact')),
                ('favorite', models.CharField(blank=True, max_length=250, null=True, verbose_name='Favorito')),
            ],
            options={
                'verbose_name': 'Apartment',
                'verbose_name_plural': 'Apartments',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Type')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Preço')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Observações')),
            ],
            options={
                'verbose_name': 'Expense',
                'verbose_name_plural': 'Expenses',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome')),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartments.Apartment', verbose_name='Apartment')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('urgency', models.CharField(choices=[('ES', 'Essential'), ('IM', 'Important'), ('DE', 'Delayable')], default='ES', max_length=10, verbose_name='Urgency')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome')),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Price (Un.)')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='Quantity')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Price (Tt.)')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('done', models.BooleanField(default=False, verbose_name='Checar')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartments.Room', verbose_name='Room')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
    ]