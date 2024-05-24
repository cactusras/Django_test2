# Generated by Django 5.0.4 on 2024-05-08 06:04

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('occupation', models.CharField(max_length=100)),
                ('notify', models.BooleanField(default=True)),
                ('pw', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('license_number', models.CharField(max_length=50, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('introduction', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(upload_to='clinics/')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('pw', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Expertise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('time', models.TimeField(default=datetime.time(1, 0))),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('photo', models.ImageField(upload_to='doctors/')),
                ('pw', models.CharField(max_length=100)),
                ('clinicID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to='myApp.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='Doc_Expertise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DocID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctorID_exp', to='myApp.doctor')),
                ('Expertise_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_exp_license', to='myApp.expertise')),
            ],
        ),
        migrations.CreateModel(
            name='Scheduling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StartDate', models.DateField()),
                ('EndDate', models.DateField()),
                ('DoctorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduling', to='myApp.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Waiting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('status', models.BooleanField(default=False)),
                ('ClientID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waitings', to='myApp.client')),
                ('SchedulingID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waitings', to='myApp.scheduling')),
                ('expertiseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waitings', to='myApp.expertise')),
            ],
        ),
        migrations.CreateModel(
            name='WorkingHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
            options={
                'ordering': ['day_of_week', 'start_time'],
                'unique_together': {('day_of_week', 'start_time', 'end_time')},
            },
        ),
        migrations.AddField(
            model_name='scheduling',
            name='WorkingHour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduling', to='myApp.workinghour'),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('Status', models.IntegerField(choices=[(0, 'reserved'), (1, 'checkin failed'), (2, 'checkin successed'), (3, 'in treatment'), (4, 'finish'), (5, 'cancelled by doc')], default=0)),
                ('ClientID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='myApp.client')),
                ('expertiseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='myApp.expertise')),
                ('SchedulingID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='myApp.scheduling')),
            ],
            options={
                'unique_together': {('ClientID', 'SchedulingID', 'Status')},
            },
        ),
    ]