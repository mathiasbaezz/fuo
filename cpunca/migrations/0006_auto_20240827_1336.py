# Generated by Django 3.2.21 on 2024-08-27 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpunca', '0005_auto_20240827_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partidounca',
            name='minuto',
        ),
        migrations.RemoveField(
            model_name='partidounca',
            name='tipo',
        ),
    ]
