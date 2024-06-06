from datetime import datetime
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
        fields = ['email', 'name', 'phone_number']

#有update的form沒有密碼跟圖片(資料更新時不更改密碼 圖片)
class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['email', 'name','phone_number','experience' ]
    def __init__(self, *args, **kwargs):
        self.update = kwargs.pop('update', False)
        super(DoctorUpdateForm, self).__init__(*args, **kwargs)

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['email', 'name','phone_number','password','photo','experience' ]
    def __init__(self, *args, **kwargs):
        self.update = kwargs.pop('update', False)
        super(DoctorForm, self).__init__(*args, **kwargs)

class ClinicUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    license_number = forms.CharField(required=True)

    class Meta:
        model = Clinic
        #fields = ['name', 'license_number','phone_number','address','introduction','photo','email','password' ]
        fields = ['email', 'name','phone_number','license_number','address','introduction']
    def __init__(self, *args, **kwargs):
        super(ClinicUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].validators = []
        self.fields['license_number'].validators = []

class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        #fields = ['name', 'license_number','phone_number','address','introduction','photo','email','password' ]
        fields = ['email', 'name','phone_number','password','license_number','address','introduction','photo']
    def __init__(self, *args, **kwargs):
        super(ClinicForm, self).__init__(*args,**kwargs)
        

class ClientUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Client
        fields = ['email', 'name', 'phone_number', 'address', 'birth_date', 'gender', 'occupation', 'notify']

    def __init__(self, *args, **kwargs):
        super(ClientUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].validators = []

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [ 'email','name','phone_number','password','address','birth_date','gender','occupation','notify']
    
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args,**kwargs)
        #self.update = kwargs.pop('update', False)

class WorkingHourForm(forms.ModelForm):
    class Meta:
        #print('form start')
        model = WorkingHour
        fields = ['day_of_week','start_time','end_time']
        #print('form finish')
        
class SchedulingForm(forms.ModelForm):
    class Meta:
        model = Scheduling
        fields = ['StartDate','EndDate']
        
class Doctor_ExpertiseForm(forms.ModelForm):
    class Meta:
        model = Doc_Expertise
        fields = ['DocID','Expertise_ID']

class ExpertiseForm(forms.ModelForm):
    class Meta:
        model = Expertise
        fields = ['name']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['ClientID','SchedulingID','expertiseID','time_start']
        
       
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
     
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class SearchForm(forms.Form):
    query = forms.CharField(label='查詢欄位', max_length=255)
    city = forms.ChoiceField(label='縣市', choices=[], required=False)
    district = forms.ChoiceField(label='地區', choices=[], required=False)
    category = forms.ChoiceField(label='治療項目', choices=[], required=False)
    treatment = forms.ChoiceField(label='具體治療', choices=[], required=False)
    start_date = forms.DateField(label='看診日期 開始', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='結束', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
