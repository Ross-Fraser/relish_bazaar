# Generated by Django 4.2.11 on 2024-05-06 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('main_category', models.CharField(max_length=100)),
                ('sub_category', models.CharField(max_length=100)),
            ],
        ),
    ]