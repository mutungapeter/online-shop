# Generated by Django 3.1 on 2023-06-25 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_totral',
            new_name='order_total',
        ),
    ]
