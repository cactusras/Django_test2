from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path('client/reserve/', views.clieReserve, name='client_reservation'),
    path('doctor/reserve/', views.docReserve, name='doctor_reserve'),
    path('clinic/reserve/', views.clinReserve, name='clinic_reserve'),
    path('client/data/edit/', views.cliedataEd, name='client_data_edit'),
    path('clinic/data/edit/', views.clinDataEd, name='clinic_data_edit'),
    path('doctor/data/edit/', views.docDataEd, name='doctor_data_edit'),
    path('click/schedule/', views.clickSchedule, name='click_to_edit_schedule'),
    path('clinic/home/', views.clinHome, name='clinic_home'),
    path('doctor/manage/', views.docManage, name='doctor_management'),
    path('doctor/page/', views.docPage, name='doctor_page'),
    path('waitinglist/to/reservation/', views.waitingToResForC, name='waiting_to_reservation'),
    path('available/', views.available, name='available_times'),
    path('doctor/reserve/<int:doc_id>/', views.doctor_reserve_page, name='doctor_reserve_page'),
    path('clinic/reserve/<int:clinic_id>/', views.clinic_reserve_page, name='clinic_reserve_page'),
    path('client/records/', views.clientRecord_loading, name='client_records'),
    path('doctor/page/loading/', views.doctorPage_loading, name='doctor_page_loading'),
    path('clinic/load/', views.clinic_load, name='clinic_load'),
    path('reservation/status/change/checkinfailed/<int:reservation_id>/', views.reservationStCF, name='reservation_status_checkin_failed'),
    path('reservation/status/change/checkinsuccessed/<int:reservation_id>/', views.reservationStSc, name='reservation_status_checkin_successed'),
    path('reservation/status/change/intreatment/<int:reservation_id>/', views.reservationStIt, name='reservation_status_in_treatment'),
    path('reservation/status/change/finished/<int:reservation_id>/', views.reservationStFn, name='reservation_status_finished'),
    path('reservation/status/change/cancelledbydoc/<int:reservation_id>/', views.reservationStCbD, name='reservation_status_cancelled_by_doctor'),
    path('doctor/clinic/search/', views.doctor_clinic_search_view, name='doctor_clinic_search'),
    path('add/reservation/', views.add_Reservation, name='add_reservation'),
    path('add/doctor/', views.add_doctor, name='add_doctor'),
    path('add/clinic/', views.add_clinic, name='add_clinic'),
    path('add/client/', views.add_client, name='add_client'),
    path('doc/expertise/upload/', views.DocExp_uploading, name='doc_expertise_upload'),
    path('doc/upload/', views.Doc_uploading, name='doc_upload'),
    path('workingHour/upload/', views.workingHour_upload, name='working_hour_upload'),
    path('scheduling/upload/', views.scheduling_upload, name='scheduling_upload'),
    path('success/', views.success, name='success'),
    path('doctor/delete/', views.delete_doctor, name='delete_doctor'),
    path('client/delete/reserve/', views.client_cancel_reservation, name='client_cancel_reservation'),
    path("login/", views.login, name="login"),
    #path("dentalLogin/", views.dentalLogin, name="dentalLogin"),
    path('login/login_view/', views.login_view, name='login_view'),
    path('clinic_info/', views.clinic_info, name='clinic_info'),
    path('check_authentication/', views.check_authentication, name='check_authentication')
]
