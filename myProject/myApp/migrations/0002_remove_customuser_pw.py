# Generated by Django 5.0.6 on 2024-05-29 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='pw',
        ),
    ]