from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("client_reservation/", views.clieReserve, name="clieReserve"),
    path("client_dataEdit/", views.cliedataEd, name="cliedataEd"),
    path("clinic_dataEdit/", views.clinDataEd, name="clinDataEd"),
    path("doctor_regis/", views.docRegis, name="docRegis"),
    path("ClicktoEditSchedule/", views.clickSchedule, name="clickSchedule"),\
    path("login/", views.login, name="login"),
    path("clinicPage/", views.clinHome, name="clinHome"),
    path("docManage/", views.docManage, name="docManage"),
    path("doctorPage/", views.docPage, name="docPage"),
    path("UserAppointmentRecords/", views.clieReserveRecord, name="clieReserveRecord"),
    path('clinic/emails/', views.get_clinics_emails, name='get_clinics_emails'),
    path('clinic/licenses/', views.get_clinics_licenses, name='get_clinics_licenses'),
    path('client/emails/', views.get_clients_emails, name='get_clients_emails'),
    path('doctor/emails/', views.get_doctors_emails, name='get_doctors_emails'),
    path('check_authentication/', views.check_authentication, name='check_authentication'),
    path('doctor/doctor_info/', views.doctor_info, name='doctor_info'),
    path('client/client_info/', views.client_info, name='client_info'),
    path('clinic/clinic_info/', views.clinic_info, name='clinic_info'),
    path('doctor/add_doctor/', views.add_doctor, name='add_doctor'),
    path('client/add_client/', views.add_client, name='add_client'),
    path('clinic/add_clinic/', views.add_clinic, name='add_clinic'),
]
