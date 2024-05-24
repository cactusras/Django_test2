from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("client_reservation/", views.clieReserve, name="clieReserve"),
    path("client_dataEdit/", views.cliedataEd, name="cliedataEd"),
    path("clinic_dataEdit/", views.clinDataEd, name="clinDataEd"),
    path("doctor_dataEdit/", views.docDataEd, name="docDataEd"),
    path("ClicktoEditSchedule/", views.clickSchedule, name="clickSchedule"),\
    path("login/", views.login, name="login"),
    path("clinicPage/", views.clinHome, name="clinHome"),
    path("docManage/", views.docManage, name="docManage"),
    path("doctorPage/", views.docPage, name="docPage"),
    path("dentalLogin/", views.dentalLogin, name="dentalLogin"),
    path("UserAppointmentRecords/", views.clieReserveRecord, name="clieReserveRecord"),
    path('clinic/isUniqueEmail_clin/', views.isUniqueEmail_clin, name='isUniqueEmail_clin'),
    path('clinic/isUniqueLicense_clin/', views.isUniqueLicense_clin, name='isUniqueLicense_clin'),
    path('client/isUniqueEmail_clie/', views.isUniqueEmail_clie, name='isUniqueEmail_clie'),
    path('doctor/isUniqueEmail_doc/', views.isUniqueEmail_doc, name='isUniqueEmail_doc'),
    path('check_authentication/', views.check_authentication, name='check_authentication'),
    path('doctor/doctor_info/', views.doctor_info, name='doctor_info'),
    path('client/client_info/', views.client_info, name='client_info'),
    path('clinic/clinic_info/', views.clinic_info, name='clinic_info'),
    path('doctor/add_doctor/', views.add_doctor, name='add_doctor'),
    path('client/add_client/', views.add_client, name='add_client'),
    path('clinic/add_clinic/', views.add_clinic, name='add_clinic'),
    path('login/login_view/', views.login_view, name='login_view'),
]
