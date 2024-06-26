# Generated by Django 4.2.6 on 2024-05-03 11:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_details_acc_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_details',
            name='acc_no',
            field=models.BigIntegerField(db_index=True, primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999999)]),
        ),
    ]
