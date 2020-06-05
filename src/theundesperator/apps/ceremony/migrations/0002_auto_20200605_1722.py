# Generated by Django 3.0.7 on 2020-06-05 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ceremony', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ceremony',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('place', models.CharField(blank=True, max_length=100, null=True, verbose_name='Place')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Cerimônia',
                'verbose_name_plural': 'Ceremonies',
            },
        ),
        migrations.CreateModel(
            name='ClothesPlanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('grooms_mom_dress_color', models.CharField(blank=True, max_length=15, null=True, verbose_name="Groom's Mom Dress Color")),
                ('brides_mom_dress_color', models.CharField(blank=True, max_length=15, null=True, verbose_name="Bride's Mom Dress Color")),
                ('kids_dress_color', models.CharField(blank=True, max_length=15, null=True, verbose_name="Kid's Dress Color")),
                ('ring_bearer_costume_color', models.CharField(blank=True, max_length=15, null=True, verbose_name='Ring Bearer Costume Color')),
                ('brides_dress', models.FileField(blank=True, null=True, upload_to='clothes_planner', verbose_name="Bride's Dress")),
                ('brides_shoes', models.FileField(blank=True, null=True, upload_to='clothes_planner', verbose_name="Bride's Shoes")),
                ('brides_hairstyle', models.FileField(blank=True, null=True, upload_to='clothes_planner', verbose_name="Bride's Hairstyle")),
                ('brides_makeup', models.FileField(blank=True, null=True, upload_to='clothes_planner', verbose_name="Bride's Makeup")),
                ('brides_hair_accessories', models.FileField(blank=True, null=True, upload_to='clothes_planner', verbose_name="Bride's Hair Acessories")),
                ('brides_body_accessories', models.FileField(blank=True, null=True, upload_to='clothes_planner', verbose_name="Bride's Body Acessories")),
                ('brides_lingerie', models.FileField(blank=True, null=True, upload_to='clothes_planner', verbose_name="Bride's Lingerie")),
                ('grooms_suit', models.FileField(blank=True, null=True, upload_to='clothes_planner', verbose_name="Groom's Suit")),
                ('grooms_shoes', models.FileField(blank=True, null=True, upload_to='clothes_planner', verbose_name="Groom's Shoes")),
            ],
            options={
                'verbose_name': 'Clothes Planner',
                'verbose_name_plural': 'Clothes Planners',
            },
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('group', models.CharField(choices=[('GFA', "Groom's Family"), ('BFA', "Bride's  Family"), ('GFR', "Groom's Friend"), ('BFR', "Bride's Friend"), ('UNW', "Don't want to invite, but have to")], max_length=40, verbose_name='Group')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('indispensability', models.PositiveSmallIntegerField(help_text='Indicates how much you really want this person to go', verbose_name='Indispensability')),
            ],
            options={
                'verbose_name': 'Guest',
                'verbose_name_plural': 'Guests',
            },
        ),
        migrations.CreateModel(
            name='Occasion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('name', models.CharField(max_length=100, verbose_name='Occasion')),
            ],
            options={
                'verbose_name': 'Occasion',
                'verbose_name_plural': 'Occasions',
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        ),
        migrations.AlterModelOptions(
            name='provider',
            options={'verbose_name': 'Fornecedor', 'verbose_name_plural': 'Fornecedores'},
        ),
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='card',
            field=models.FileField(blank=True, null=True, upload_to='files/', verbose_name='Cartão'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ceremony.Category', verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='favorite',
            field=models.BooleanField(verbose_name='Favorito'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Observações'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='phone',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Telefone'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Preço'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='website',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Site'),
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('name', models.CharField(max_length=50, verbose_name='Song Nome')),
                ('duration', models.TimeField(blank=True, null=True, verbose_name='Song duration')),
                ('link', models.CharField(blank=True, max_length=150, null=True, verbose_name='Link to the song')),
                ('occasion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ceremony.Occasion', verbose_name='Occasion')),
            ],
            options={
                'verbose_name': 'Music',
                'verbose_name_plural': 'Musics',
            },
        ),
        migrations.CreateModel(
            name='Groomsman',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('selector', models.CharField(choices=[('GR', 'Groom'), ('BR', 'Bride')], help_text='Who chose the groomsman', max_length=6, verbose_name='Sponsored')),
                ('name', models.CharField(max_length=50, verbose_name='Song Nome')),
                ('duo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ceremony.Groomsman', verbose_name='Duo')),
            ],
            options={
                'verbose_name': 'Groomsman',
                'verbose_name_plural': 'Groomsmen',
            },
        ),
    ]
