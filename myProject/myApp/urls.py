from . import views
from django.urls import path

urlpatterns = [
    #home之後路徑要設成login
    path("", views.home, name="home"),
    path("client_regis/", views.clieRegis, name="clieRegis"),
    path("client_reservation/", views.clieReserve, name="clieReserve"),
    path("client_dataEdit/", views.cliedataEd, name="cliedataEd"),
    path("clinic_regis/", views.clinRegis, name="clinRegis"),
    path("clinic_dataEdit/", views.clinDataEd, name="clinDataEd"),
    path("doctor_regis/", views.docRegis, name="docRegis"),
    path("ClicktoEditSchedule/", views.clickSchedule, name="clickSchedule"),
    #用google排班表 我比較傾向這個
    path("ClicktoEditScheduleGoogle/", views.clickScheduleGg, name="clickScheduleGg"),
    path("clinicPage/", views.clinHome, name="clinHome"),
    path("clinic_login_docManage/", views.clinLoginDocManage, name="clinLoginDocManage"),
    path("doctorPage/", views.docPage, name="docPage"),
    path("searchPage/", views.home, name="home"),
    path("UserAppointmentRecords/", views.clieReserveRecord, name="clieReserveRecord"),
]
