# Generated by Django 4.2.16 on 2024-11-29 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_color_color_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discription',
            field=models.TextField(blank=True, null=True),
        ),
    ]
