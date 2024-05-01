from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=50)

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
    


    
    

    
    
    

    
