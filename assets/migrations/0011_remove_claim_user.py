# Generated by Django 4.1.7 on 2023-03-05 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0010_claim'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='user',
        ),
    ]