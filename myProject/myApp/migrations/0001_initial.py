# Generated by Django 5.0.6 on 2024-05-26 07:07

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='docClinicSearch',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('doc_id', models.IntegerField()),
                ('doc_name', models.CharField(max_length=100)),
                ('clinic_id', models.IntegerField()),
                ('clinic_name', models.CharField(max_length=100)),
                ('clinic_adress', models.TextField()),
                ('clinic_introduction', models.TextField(blank=True, null=True)),
                ('exp_id', models.IntegerField()),
                ('exp_name', models.CharField(max_length=100)),
                ('scheduling_id', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('workinghour_id', models.IntegerField()),
                ('day_of_week', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
            options={
                'db_table': 'docClinicSearch',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=35)),
                ('pw', models.CharField(max_length=128)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
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
            name='Client',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('address', models.TextField(blank=True, null=True)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('notify', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('myApp.customuser',),
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('license_number', models.CharField(max_length=50, unique=True)),
                ('address', models.TextField()),
                ('introduction', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='clinics/')),
            ],
            options={
                'abstract': False,
            },
            bases=('myApp.customuser',),
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='doctors/')),
                ('exoerience', models.TextField(blank=True, null=True)),
                ('clinicID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='myApp.clinic')),
            ],
            options={
                'abstract': False,
            },
            bases=('myApp.customuser',),
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
        migrations.CreateModel(
            name='Scheduling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StartDate', models.DateField()),
                ('EndDate', models.DateField()),
                ('WorkingHour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduling', to='myApp.workinghour')),
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
                ('SchedulingID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waitings', to='myApp.scheduling')),
                ('expertiseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waitings', to='myApp.expertise')),
                ('ClientID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waitings', to='myApp.client')),
            ],
        ),
        migrations.CreateModel(
            name='Doc_Expertise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Expertise_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_exp_license', to='myApp.expertise')),
                ('DocID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctorID_exp', to='myApp.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('Status', models.IntegerField(choices=[(0, 'reserved'), (1, 'checkin failed'), (2, 'checkin successed'), (3, 'in treatment'), (4, 'finish'), (5, 'cancelled by doc')], default=0)),
                ('expertiseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='myApp.expertise')),
                ('SchedulingID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='myApp.scheduling')),
                ('ClientID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='myApp.client')),
            ],
            options={
                'unique_together': {('ClientID', 'SchedulingID', 'Status')},
            },
        ),
    ]