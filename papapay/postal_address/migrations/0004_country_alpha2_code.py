# Generated by Django 5.0 on 2023-12-29 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postal_address', '0003_rename_initials_country_alpha3_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='alpha2_code',
            field=models.CharField(blank=True, max_length=2),
        ),
    ]