# Generated by Django 4.0.3 on 2022-05-11 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_and_reservation', '0002_remove_reservation_item_remove_reservation_quantity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reserveditem',
            old_name='reservation',
            new_name='reservation_number',
        ),
    ]