# Generated by Django 4.0.4 on 2022-05-24 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_account_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='otp',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
