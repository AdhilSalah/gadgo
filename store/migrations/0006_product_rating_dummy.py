# Generated by Django 4.0.4 on 2022-06-14 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating_dummy',
            field=models.IntegerField(null=True),
        ),
    ]
