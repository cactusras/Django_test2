from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import WorkingHour,Scheduling,Doc_Expertise,Reservation,Waiting,Client,Clinic,Doctor,Expertise
from .models import CustomUser
from django.contrib.auth import authenticate

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'phone_number', 'password']


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['email', 'name','phone_number','password','photo' ]
    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args,**kwargs)
        self.fields['is_active'].initial = True
        self.fields['is_admin'].initial = False
        
class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        #fields = ['name', 'license_number','phone_number','address','introduction','photo','email','pw' ]
        fields = ['email', 'name','phone_number','password','license_number','address','introduction','photo']
    def __init__(self, *args, **kwargs):
        super(ClinicForm, self).__init__(*args,**kwargs)
        
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [ 'email','name','phone_number','password','address','birth_date','gender','occupation','notify']
    
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args,**kwargs)
        # self.fields['is_active'].initial = True
        # self.fields['is_admin'].initial = False

class WorkingHourForm(forms.ModelForm):
    class Meta:
        model = WorkingHour
        fields = ['day_of_week','start_time','end_time']
        
class SchedulingForm(forms.ModelForm):
    class Meta:
        model = Scheduling
        fields = ['StartDate','EndDate']
        
#class Doctor_ExpertiseForm(forms.ModelForm):
#    class Meta:
#        model = Doc_Expertise
#        fields = ['DocID','Expertise_ID']

class ExpertiseForm(forms.ModelForm):
    class Meta:
        model = Expertise
        fields = ['name']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['ClientID','SchedulingID','expertiseID','time_start','time_end','Status']
        
       
class WaitingForm(forms.ModelForm):
    class Meta:
        model = Waiting
        fields = ['ClientID','SchedulingID','expertiseID','time_start','time_end','status']
        
        
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)