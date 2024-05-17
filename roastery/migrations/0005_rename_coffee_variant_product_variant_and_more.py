# Generated by Django 4.2.11 on 2024-05-16 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roastery', '0004_coffee_grind_coffee_origin_coffee_size_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='coffee_variant',
            new_name='variant',
        ),
        migrations.AlterField(
            model_name='coffee_origin',
            name='region',
            field=models.IntegerField(choices=[(0, 'Sidamo'), (1, 'Blue Mountain'), (2, 'Agua Santa'), (3, 'Excelso Popayan'), (4, 'Huehuetenango'), (5, 'Copaceyba'), (6, 'Malabar'), (7, '-')]),
        ),
    ]
