# Generated by Django 4.0.4 on 2022-06-14 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
