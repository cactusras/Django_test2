from django import forms
from .models import Doctor 

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['License', 'Name', 'Degree', 'Experience', 'Phone', 'Time_table', 'Photo']
