# Generated by Django 3.2.8 on 2021-11-17 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basket',
            old_name='quantity_in_basket',
            new_name='quantity',
        ),
    ]