# Generated by Django 4.1.7 on 2023-03-03 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_itemdata_the_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemdata',
            name='the_date',
        ),
    ]