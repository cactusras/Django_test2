from django.db import models
from datetime import timedelta
from datetime import time

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    introduction = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='clinics/')
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='doctors/')
    degree = models.CharField(max_length=100)
   
    
    def __str__(self):
        return self.name

class Expertise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    time = models.TimeField(default=time(hour=1))

    def __str__(self):
        return self.name


class Doc_Expertise(models.Model):
    DocID = models.ForeignKey(
        Doctor,
        on_delete = models.SET_NULL,
        null = True,
        related_name='doctorID_exp'
    )
    Expertise_ID = models.ForeignKey(
        Expertise,
        on_delete = models.SET_NULL,
        null = True,
        related_name='doctor_exp_license'
    )


    
class Hiring(models.Model):
    clinic = models.ForeignKey(Clinic, related_name='hirings', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='hirings', on_delete=models.CASCADE)
    #start_date = models.DateField()
    #end_date = models.DateField(blank=True, null=True)
    #working_hours = models.CharField(max_length=100)  # Example: '9AM-5PM'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['clinic', 'doctor'], name='unique_clinic_doctor')
        ]

    def __str__(self):
        return f"{self.doctor.name} at {self.clinic.name}"

class Reservation(models.Model):
    Client = models.ForeignKey('Client', related_name='reservations', on_delete=models.CASCADE)
    WorkingHour = models.ForeignKey('WorkingHour', related_name='reservations', on_delete=models.CASCADE)
    expertise = models.ForeignKey('Expertise', related_name='reservations', on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    #check_in = models.BooleanField(default=False)
    STATUS_CHOICES = (
        (0, 'reserved'),
        (1, 'checkin failed'),
        (2, 'checkin successed'),
        (3, 'in treatment'),
        (4, 'finish')
    )
    
    Status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    

    def __str__(self):
        return f"{self.client.name} reservation for {self.hiring}"

class Waiting(models.Model):
    Client = models.ForeignKey('Client', related_name='waitings', on_delete=models.CASCADE)
    hiring = models.ForeignKey('Hiring', related_name='waitings', on_delete=models.CASCADE)
    expertise = models.ForeignKey('Expertise', related_name='waitings', on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client.name} waiting for {self.hiring}"

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    occupation = models.CharField(max_length=100)
    notify = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class WorkingHour(models.Model):
    DAY_CHOICES = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday')
    ]

    hiring = models.ForeignKey('Hiring', related_name='working_hours', on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('hiring', 'day_of_week', 'start_time', 'end_time')
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        day_name = dict(self.DAY_CHOICES)[self.day_of_week]
        return f"{day_name}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"




