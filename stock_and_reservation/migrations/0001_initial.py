# Generated by Django 4.0.3 on 2022-05-02 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='E-mailová adresa')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Uživatelské jméno')),
                ('organisation_name', models.CharField(max_length=100, unique=True, verbose_name='Název organizace')),
                ('contact_person', models.CharField(blank=True, max_length=50, verbose_name='Kontaktní osoba')),
                ('address', models.CharField(blank=True, max_length=200, verbose_name='Adresa')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='Telefon')),
                ('notes', models.TextField(blank=True, verbose_name='Poznámky')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superadmin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Organizace',
                'verbose_name_plural': 'Organizace',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100, verbose_name='název')),
                ('description', models.TextField(blank=True, max_length=500, verbose_name='popis')),
                ('image', models.ImageField(blank=True, upload_to='')),
            ],
            options={
                'verbose_name': 'Položka',
                'verbose_name_plural': 'Položky',
            },
        ),
        migrations.CreateModel(
            name='ItemVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('32', '32'), ('44', '44'), ('52', '52')], max_length=50, verbose_name='velikost')),
                ('fabric_design', models.CharField(choices=[('uni', 'uni'), ('dívčí', 'dívčí'), ('chlapecký', 'chlapecký')], max_length=50, verbose_name='vzor')),
                ('description', models.TextField(blank=True, max_length=500, verbose_name='popis')),
                ('on_stock', models.PositiveIntegerField(verbose_name='na skladě')),
                ('reserved_quantity', models.IntegerField(verbose_name='rezervované množství')),
                ('saldo', models.IntegerField(blank=True, editable=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_and_reservation.item', verbose_name='položka')),
            ],
            options={
                'verbose_name': 'Varianta',
                'verbose_name_plural': 'Varianty',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('created_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now, verbose_name='vytvořena dne')),
                ('reservation_number', models.IntegerField(auto_created=True, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='rezervační číslo')),
                ('status', models.CharField(choices=[('new', 'nová'), ('in progress', 'rozpracovaná'), ('completed', 'připravená k odeslání'), ('closed', 'uzavřená')], default='new', max_length=50)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='upravena dne')),
                ('quantity', models.IntegerField(verbose_name='počet kusů')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_and_reservation.itemvariation', verbose_name='položka')),
                ('organisation_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='organizace')),
            ],
            options={
                'verbose_name': 'Rezervace',
                'verbose_name_plural': 'Rezervace',
            },
        ),
    ]