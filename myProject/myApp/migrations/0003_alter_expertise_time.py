# Generated by Django 5.0.6 on 2024-06-02 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0002_rename_exoerience_doctor_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expertise',
            name='time',
            field=models.DurationField(),
        ),
    ]