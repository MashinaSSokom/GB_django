# Generated by Django 3.2.8 on 2021-11-12 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20211112_1840'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopuserprofile',
            options={'ordering': ['id'], 'verbose_name': 'Профиль пользователя', 'verbose_name_plural': 'Профили пользователей'},
        ),
    ]