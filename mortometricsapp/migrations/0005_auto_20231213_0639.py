# Generated by Django 3.0.3 on 2024-12-13 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mortometricsapp', '0004_mortalityrate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mortalityrate',
            old_name='country_name',
            new_name='country_data',
        ),
        migrations.RemoveField(
            model_name='mortalityrate',
            name='country_code',
        ),
    ]
