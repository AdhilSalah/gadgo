# Generated by Django 4.0.4 on 2022-05-27 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartId',
            new_name='CartItem',
        ),
    ]
