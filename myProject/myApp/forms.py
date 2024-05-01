from django import forms
from .models import Doctor
from .models import Clinic

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'email','phone_number','photo','degree' ]
        
class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'license_number','phone_number','address','introduction','photo','email' ]


