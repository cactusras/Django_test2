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


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['email', 'name','phone_number','password','photo','experience']
    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args,**kwargs)

        
class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        #fields = ['name', 'license_number','phone_number','address','introduction','photo','email','password' ]
        fields = ['email', 'name','phone_number','password','license_number','address','introduction','photo']
    def __init__(self, *args, **kwargs):
        super(ClinicForm, self).__init__(*args,**kwargs)
      #  self.fields['is_active'].initial = True
      #  self.fields['is_admin'].initial = False
        
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
       #fields = ['ClientID','SchedulingID','expertiseID','time_start','time_end','Status']
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

class TestingForm(forms.Form):
    doctor_id = forms.IntegerField(label='Doctor ID')
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    expertise_name = forms.CharField(label='Expertise Name', max_length=100)
    expertise_list = forms.CharField(label='Expertise List', widget=forms.Textarea)
    
    
class DoctorUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Doctor
        fields = ['email', 'name','phone_number','password','photo','experience']
    def __init__(self, *args, **kwargs):
        super(DoctorUpdateForm, self).__init__(*args,**kwargs)
        self.fields['email'].validators = []
    
    def clean_email(self):
        email = self.data.get('email')
        return email
    def is_valid(self):
        valid = super(DoctorUpdateForm, self).is_valid()
        email = self.data.get('email')
        self.cleaned_data['email'] = email  # Add raw email to cleaned_data
        valid=True

        # Return True regardless of email validation
        return valid

class ClinicUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    license_number = forms.CharField(required=True)

    class Meta:
        model = Clinic
        fields = ['email', 'name','phone_number','license_number','address','introduction']
    def __init__(self, *args, **kwargs):
        super(ClinicUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].validators = []
        self.fields['license_number'].validators = []
        

class ClientUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Client
        fields = ['email', 'name', 'phone_number', 'address', 'birth_date', 'gender', 'occupation', 'notify']

    def __init__(self, *args, **kwargs):
        super(ClientUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].validators = []



# class LoginForm(forms.Form):
#     email = forms.EmailField(label=_("Email"))
#     password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

#     error_messages = {
#         'invalid_login': _(
#             "Please enter a correct email address and password. Note that both "
#             "fields may be case-sensitive."
#         ),
#         'inactive': _("This account is inactive."),
#     }
    
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)

#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')
#         password = cleaned_data.get('password')

#         if email is not None and password:
#             self.user_cache = authenticate(self.request, email=email, password=password)
            
#             if not self.user_cache:
#                 raise forms.ValidationError('Invalid email or password.')

#             # if self.user_cache is None:
#             #     raise forms.ValidationError(
#             #         self.error_messages['invalid_login'],
#             #         code='invalid_login',
#             #         params={'email': self.fields.verbose_name},
#             #     )
#             # elif not self.user_cache.is_active:
#             #     raise forms.ValidationError(self.error_messages['inactive'], code='inactive')
#         return cleaned_data

#     def get_user(self):
#         return self.user_cache
        
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
