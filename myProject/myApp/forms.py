from django import forms
from .models import Doctor
from .models import Clinic
from .models import Client
from .models import WorkingHour
from .models import Scheduling
from .models import Doc_Expertise


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        #fields = ['name', 'email','phone_number','photo','degree','clinicID' ]
        fields = ['name', 'email','phone_number','photo','clinicID','pw' ]
        
        
class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'license_number','phone_number','address','introduction','photo','email','pw' ]
        
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email','phone_number','address','birth_date','gender','occupation','notify','pw']

class WorkingForm(forms.ModelForm):
    class Meta:
        model = WorkingHour
        fields = ['day_of_week','start_time','end_time']
        
class SchedulingForm(forms.ModelForm):
    class Meta:
        model = Scheduling
        fields = ['DoctorID','WorkingHour','StartDate','EndDate']
        
class Doctor_Expertise(forms.ModelForm):
    class Meta:
        model = Doc_Expertise
        fields = ['DocID','Expertise_ID']
        

    