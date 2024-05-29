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
        fields = ['email', 'name', 'phone_number', 'pw']


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['email', 'name','phone_number','pw','photo' ]
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
        
        
#django自帶login
class AuthenticationForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	error_messages = {
		'invalid_login': _(
			"Please enter a correct %(username)s and password. Note that both "
			"fields may be case-sensitive."
		),
		'inactive': _("This account is inactive."),
	}

	def __init__(self, request=None, *args, **kwargs):
		self.request = request
		self.user_cache = None
		super().__init__(*args, **kwargs)
		self.username_field = User._meta.get_field(User.USERNAME_FIELD)
		self.fields['username'].label = self.username_field.verbose_name
		self.fields['username'].max_length = self.username_field.max_length or 254
		if self.fields['username'].label is None:
			self.fields['username'].label = _('Username')

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username is not None and password:
			self.user_cache = authenticate(self.request, username=username, password=password)
			if self.user_cache is None:
				raise forms.ValidationError(
					self.error_messages['invalid_login'],
					code='invalid_login',
					params={'username': self.username_field.verbose_name},
				)
			else:
				self.confirm_login_allowed(self.user_cache)

		return self.cleaned_data

	def confirm_login_allowed(self, user):
		if not user.is_active:
			raise forms.ValidationError(
				self.error_messages['inactive'],
				code='inactive',
			)

	def get_user(self):
		return self.user_cache

	def get_user_id(self):
		if self.user_cache:
			return self.user_cache.id
		return None