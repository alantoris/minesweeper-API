# Generated by Django 3.1.6 on 2021-02-17 19:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0003_match_remaining_free_cells'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='height',
            field=models.PositiveIntegerField(default=20, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(50)]),
        ),
        migrations.AlterField(
            model_name='match',
            name='width',
            field=models.PositiveIntegerField(default=20, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(50)]),
        ),
    ]
