# Generated by Django 5.0.4 on 2024-05-01 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0002_delete_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('ClinicID', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('ClinicName', models.CharField(max_length=200)),
                ('Address', models.CharField(max_length=200)),
                ('Phone', models.CharField(max_length=200)),
                ('Info', models.CharField(max_length=200)),
            ],
        ),
    ]
