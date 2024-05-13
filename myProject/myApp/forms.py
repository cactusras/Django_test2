from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Doctor
from .models import Clinic
from .models import Client
from .models import WorkingHour
from .models import Scheduling
from .models import Doc_Expertise
from .models import Reservation
from .models import Waiting
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'phone_number', 'pw']


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        #fields = ['name', 'email','phone_number','photo','degree','clinicID' ]
        fields = ['email', 'name','phone_number','pw','photo','clinicID' ]
    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args,**kwargs)
        self.fields['is_active'].initial = True
        self.fields['is_admin'].initial = False
        
class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        #fields = ['name', 'license_number','phone_number','address','introduction','photo','email','pw' ]
        fields = ['email', 'name','phone_number','pw','license_number','address','introduction','photo']
    def __init__(self, *args, **kwargs):
        super(ClinicForm, self).__init__(*args,**kwargs)
        self.fields['is_active'].initial = True
        self.fields['is_admin'].initial = False
        
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [ 'email','name','phone_number','pw','address','birth_date','gender','occupation','notify']
    
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args,**kwargs)
        self.fields['is_active'].initial = True
        self.fields['is_admin'].initial = False

class WorkingHourForm(forms.ModelForm):
    class Meta:
        model = WorkingHour
        fields = ['day_of_week','start_time','end_time']
        
class SchedulingForm(forms.ModelForm):
    class Meta:
        model = Scheduling
        fields = ['DoctorID','WorkingHour','StartDate','EndDate']
        
class Doctor_ExpertiseForm(forms.ModelForm):
    class Meta:
        model = Doc_Expertise
        fields = ['DocID','Expertise_ID']
        
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['ClientID','SchedulingID','expertiseID','time_start','time_end','Status']
        
       
class WaitingForm(forms.ModelForm):
    class Meta:
        model = Waiting
        fields = ['ClientID','SchedulingID','expertiseID','time_start','time_end','status']
        
        

    
