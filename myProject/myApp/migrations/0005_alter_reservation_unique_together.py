# Generated by Django 5.0.6 on 2024-06-03 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0004_alter_expertise_time'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('ClientID', 'time_start', 'SchedulingID', 'Status')},
        ),
    ]
