from django.db import models

# Create your models here.

class Clinic(models.Model):
    ClinicID = models.CharField(max_length=200, primary_key=True)
    ClinicName = models.CharField(max_length=200)
    Address = models.CharField(max_length=200)
    Phone = models.CharField(max_length=200)
    Info = models.CharField(max_length=200)

    def __str__(self):
        return self.ClinicName
    
class Doctor(models.Model):
    License = models.CharField(max_length=200, primary_key=True)
    Name = models.CharField(max_length=200)
    Degree = models.CharField(max_length=200)
    Experience = models.CharField(max_length=200)
    Phone = models.CharField(max_length=200)
    Time_table = models.DateTimeField()
    Photo = models.ImageField(upload_to='doctor_photos/', default='')

class Hiring(models.Model):
    ClinicID = models.ForeignKey(
        Clinic,
        on_delete = models.SET_NULL,
        null = True,
        related_name='clinic_hiring'
    )
    DoctorLicense = models.ForeignKey(
        Doctor,
        on_delete = models.SET_NULL,
        null = True,
        related_name='doctor_hiring'
    )
    Time_table = models.DateTimeField()
    
class Expertise(models.Model):
    Expertise_ID=models.AutoField(primary_key=True)
    Treating_Time = models.TimeField()
    Expertise_Name = models.CharField(max_length=200)

class Doc_Expertise(models.Model):
    Doctor_License = models.ForeignKey(
        Doctor,
        on_delete = models.SET_NULL,
        null = True,
        related_name='doctor_license_exp'
    )
    Expertise_ID = models.ForeignKey(
        Expertise,
        on_delete = models.SET_NULL,
        null = True,
        related_name='doctor_exp_license'
    )

class Client(models.Model):
    Client_email =  models.CharField(max_length=200, primary_key=True)
    Gender = models.CharField(max_length=5)
    Phone = models.CharField(max_length=200)
    Name = models.CharField(max_length=200)
    Occupation = models.CharField(max_length=200)
    Birth = models.DateField()
    Checking_Notification = models.BooleanField()
    
class Waiting(models.Model):
    Client_email = models.ForeignKey(
        Client,
        on_delete = models.SET_NULL,
        null = True,
        related_name='waiting_client'
    )
    Doctor_License = models.ForeignKey(
        Doctor,
        on_delete = models.SET_NULL,
        null = True,
        related_name='waiting_reservation_doc'
    )
    Clinic_ID= models.ForeignKey(
        Clinic,
        on_delete = models.SET_NULL,
        null = True,
        related_name='waiting_reservation_clinic'
    )
    Exp_ID= models.ForeignKey(
        Expertise,
        on_delete = models.SET_NULL,
        null = True,
        related_name='waiting_reservation_Exp'
    )
    Time = models.DateTimeField()
    Status = models.BooleanField()
    
    
class Reservation(models.Model):
    Client_email = models.ForeignKey(
        Client,
        on_delete = models.SET_NULL,
        null = True,
        related_name='rsv_client'
    )
    Doctor_License = models.ForeignKey(
        Doctor,
        on_delete = models.SET_NULL,
        null = True,
        related_name='reservation_doc'
    )
    Clinic_ID= models.ForeignKey(
        Clinic,
        on_delete = models.SET_NULL,
        null = True,
        related_name='reservation_clinic'
    )
    Exp_ID= models.ForeignKey(
        Expertise,
        on_delete = models.SET_NULL,
        null = True,
        related_name='eservation_Exp'
    )
    Time = models.DateTimeField()
    STATUS_CHOICES = (
        (0, 'reserved'),
        (1, 'checkin failed'),
        (2, 'checkin successed'),
        (3, 'in treatment'),
        (3, 'finish')
    )
    Status = models.IntegerField(choices=STATUS_CHOICES, default=0)




    
    

    
    
    

    
