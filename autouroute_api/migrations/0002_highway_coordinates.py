# Generated by Django 5.1.4 on 2025-01-18 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autouroute_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='highway',
            name='coordinates',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
