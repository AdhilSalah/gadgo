# Generated by Django 4.0.4 on 2022-05-24 07:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_otp_alter_account_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
