# Generated by Django 3.1 on 2023-08-09 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20230730_1318'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sellitem',
            old_name='address_line_1',
            new_name='current_location',
        ),
        migrations.RenameField(
            model_name='sellitem',
            old_name='first_name',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='sellitem',
            old_name='address_line_2',
            new_name='town',
        ),
        migrations.RemoveField(
            model_name='sellitem',
            name='email',
        ),
        migrations.RemoveField(
            model_name='sellitem',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='sellitem',
            name='street',
        ),
    ]
