# Generated by Django 4.2.2 on 2023-06-14 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_store_utc_offset'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='utc_offset',
            new_name='timezone',
        ),
    ]
