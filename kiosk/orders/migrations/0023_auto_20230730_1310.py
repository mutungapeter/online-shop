# Generated by Django 3.1 on 2023-07-30 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20230730_1310'),
        ('orders', '0022_auto_20230730_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]