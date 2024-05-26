from django.db import models
from datetime import timedelta
from datetime import time
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
#PK皆Auto Increment

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

# 定義自定義的使用者管理器
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, phone_number, pw=None):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number,
        )
        user.set_password(pw)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone_number, pw=None):
        user = self.create_user(
            email=email,
            name=name,
            phone_number=phone_number,
            pw=pw,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# 自定義的使用者模型
class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=35)
    pw = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

class Client(CustomUser):
   
    address = models.TextField(null=True,blank=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    occupation = models.CharField(max_length=100,null=True,blank=True)
    notify = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Clinic(CustomUser):
   
    license_number = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    introduction = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='clinics/',blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Doctor(CustomUser):
    
    photo = models.ImageField(upload_to='doctors/',null=True,blank=True)
    clinicID = models.ForeignKey('Clinic', related_name='doctors', on_delete=models.CASCADE)  # 與 Clinic 關聯
    exoerience = models.TextField(null=True,blank=True)
    

    def __str__(self):
        return self.name

class Expertise(models.Model):
    
    name = models.CharField(max_length=100)
    time = models.TimeField(default=time(hour=1))

    def __str__(self):
        return self.name

class Doc_Expertise(models.Model):
    DocID = models.ForeignKey(
        Doctor,
        on_delete = models.CASCADE,
        #on_delete = models.SET_NULL,
        #null = True,
        related_name='doctorID_exp'
    )
    Expertise_ID = models.ForeignKey(
        Expertise,
        on_delete = models.CASCADE,
        #on_delete = models.SET_NULL,
        #null = True,
        related_name='doctor_exp_license'
    )
     
class Scheduling(models.Model):
    DoctorID = models.ForeignKey('Doctor', related_name='scheduling', on_delete=models.CASCADE)
   #Reservation = models.ForeignKey('Reservation', related_name='scheduling', on_delete=models.CASCADE)
    WorkingHour = models.ForeignKey('WorkingHour', related_name='scheduling', on_delete=models.CASCADE)
    StartDate = models.DateField()
    EndDate = models.DateField()
    
    def WDforFront(self):
        return self.StartDate.weekday() + 1
    
    def TimeSlotNumber(self):
        duration = self.time_end - self.time_start
        total_hours = int(duration.total_seconds() // 3600)  # Total hours between start and end
        slot_numbers = [i + 1 for i in range(total_hours)]  # Generate slot numbers for each hour
        return slot_numbers
    
     
class Reservation(models.Model):
    ClientID = models.ForeignKey('Client', related_name='reservations', on_delete=models.CASCADE)
    SchedulingID = models.ForeignKey('Scheduling', related_name='reservations', on_delete=models.CASCADE)
    expertiseID = models.ForeignKey('Expertise', related_name='reservations', on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    #check_in = models.BooleanField(default=False)
    STATUS_CHOICES = (
        (0, 'reserved'),
        (1, 'checkin failed'),
        (2, 'checkin successed'),
        (3, 'in treatment'),
        (4, 'finish'),
        (5, 'cancelled by doc')
    )
    
    Status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    
    class Meta:
        unique_together = ('ClientID', 'SchedulingID', 'Status')
    
    #原本應該是直觀用來看客戶醫生診所預約關係
    #改成scheduling之後應該就變成直觀能看到醫生不一定有診所
    def __str__(self):
        return f"{self.client.name} reservation for doctor{self.SchedulingID.DoctorID}, clinic {self.SchedulingID.DoctorID.clnicID}"
    
    def update_status(self, new_status):
        if new_status in self.STATUS_CHOICES:
            self.Status = new_status
            self.save()
        else:
            raise ValueError("Invalid status value")
        
    def get_status_display(self):
        return self.Status

    def WDforFront(self):
        return self.StartDate.weekday() + 1
    
    def TimeSlotNumber(self):
        duration = self.time_end - self.time_start
        total_hours = int(duration.total_seconds() // 3600)  # Total hours between start and end
        slot_numbers = [i + 1 for i in range(total_hours)]  # Generate slot numbers for each hour
        return slot_numbers
    
class Waiting(models.Model):
    ClientID = models.ForeignKey('Client', related_name='waitings', on_delete=models.CASCADE)
    SchedulingID = models.ForeignKey('Scheduling', related_name='waitings', on_delete=models.CASCADE)
    expertiseID = models.ForeignKey('Expertise', related_name='waitings', on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    #等待中是否等到
    status = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.client.name} waiting for doctor{self.SchedulingID.DoctorID}, clinic {self.SchedulingID.DoctorID.clnicID}"


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

    #hiring = models.ForeignKey('Hiring', related_name='working_hours', on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('day_of_week', 'start_time', 'end_time')
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        day_name = dict(self.DAY_CHOICES)[self.day_of_week]
        return f"{day_name}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
    
    
class docClinicSearch(models.Model):
    DAY_CHOICES = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday')
    ]
    id = models.CharField(max_length=255, primary_key=True)
    doc_id = models.IntegerField()  #d.id
    doc_name = models.CharField(max_length=100) #d.name    
    clinic_id = models.IntegerField() #d.clinicid
    clinic_name = models.CharField(max_length=100)  #c.name
    clinic_adress = models.TextField()#c.adress
    clinic_introduction = models.TextField(blank=True, null=True)#c.introduction
    exp_id = models.IntegerField()#e.id
    exp_name = models.CharField(max_length=100)#e.name
    scheduling_id = models.IntegerField()#ms.id
    start_date = models.DateField()#ms.start_date
    end_date = models.DateField()#ms.end_date
    workinghour_id = models.IntegerField()#w.WorkingHour_id
    day_of_week = models.IntegerField(choices=DAY_CHOICES)#w.day_of_week
    start_time = models.TimeField()#w.start_time
    end_time = models.TimeField()#w.end_time
    
    class Meta:
        managed = False  # No migrations will be made for this model
        db_table = 'docClinicSearch'  # Name of the view in the database

#docClinicSearch: AutoField to IntegerField, and PK? 