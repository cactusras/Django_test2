from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    #login logout
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    #註冊
    path('isUniqueEmail_clin/', views.isUniqueEmail_clin, name='isUniqueEmail_clin'),
    path('isUniqueLicense_clin/', views.isUniqueLicense_clin, name='isUniqueLicense_clin'),
    path('isUniqueEmail_clie/', views.isUniqueEmail_clie, name='isUniqueEmail_clie'),
    path('isUniqueEmail_doc/', views.isUniqueEmail_doc, name='isUniqueEmail_doc'),
    path('add/client/', views.add_client, name='add_client'),
    path('add/reservation/', views.add_Reservation, name='add_reservation'),
    path('add/clinic/', views.add_clinic, name='add_clinic'),
    #handle_upload_file
    path('doc/upload/', views.Doc_uploading, name='doc_upload'),
    path('doc/expertise/upload/', views.DocExp_uploading, name='doc_expertise_upload'),
    path('workingHour/upload/', views.workingHour_upload, name='working_hour_upload'),
    path('scheduling/upload/', views.scheduling_upload, name='scheduling_upload'),
    path('doc/session/', views.doc_session, name='doc_session'),
    path('add/doctor/', views.add_doctor, name='add_doctor'),
    path('success/', views.success, name='success'),
    path('doctor/delete/<str:doctor_email>/', views.delete_doctor, name='delete_doctor'),
    path('doctor/clinic/search/', views.doctor_clinic_search_view, name='doctor_clinic_search'),

    #預約
    #get_time_slots
    path('reservation/status/change/checkinfailed/<int:reservation_id>/', views.reservationStCF, name='reservation_status_checkin_failed'),
    path('reservation/status/change/checkinsuccessed/<int:reservation_id>/', views.reservationStSc, name='reservation_status_checkin_successed'),
    path('reservation/status/change/intreatment/<int:reservation_id>/', views.reservationStIt, name='reservation_status_in_treatment'),
    path('reservation/status/change/finished/<int:reservation_id>/', views.reservationStFn, name='reservation_status_finished'),
    path('reservation/status/change/cancelledbydoc/<int:reservation_id>/', views.reservationStCbD, name='reservation_status_cancelled_by_doctor'),
    path('doctor/reserve/<int:doc_id>/', views.doctor_reserve_page, name='doctor_reserve_page'),
    path('clinic/reserve/<int:clinic_id>/', views.clinic_reserve_page, name='clinic_reserve_page'),
    path('clinic/doctor/<int:doctor_id>/reserve/', views.clinic_reserve_doctor_confirmed, name='clinic_reserve_doctor_confirmed'),
    #add_time
    path('available/', views.available, name='available_times'),
    path('waitinglist/to/reservation/', views.waitingToResForC, name='waiting_to_reservation'),
    path('client/delete/reserve/', views.client_cancel_reservation, name='client_cancel_reservation'),
    path('check_reservations/', views.check_reservations, name='check_reservations'),

    #頁面載入、跳轉
    path('clinic/load/', views.clinic_load, name='clinic_load'),
    path('doctor/page/loading/', views.doctorPage_loading, name='doctor_page_loading'),
    path('client/records/', views.clientRecord_loading, name='client_records'),
    path('home/',views.home, name = 'home'),
    path('client/reserve/', views.clieReserve, name='client_reservation'),
    path('client/data/edit/', views.cliedataEd, name='client_data_edit'),
    path('clinic/data/edit/', views.clinDataEd, name='clinic_data_edit'),
    path('doctor/data/edit/', views.docDataEd, name='doctor_data_edit'),
    path('click/schedule/', views.clickSchedule, name='click_to_edit_schedule'),
    path('click/schedule/new/', views.clickScheduleNew, name='click_to_edit_schedule_new'),
    path('loginP/', views.loginP, name='loginP'),
    path('clinic/home/', views.clinHome, name='clinic_home'),
    path('doctor/manage/', views.docManage, name='doctor_management'),
    path('doctor/page/', views.docPage, name='doctor_page'),
    path('clieReserveRecord/', views.clieReserveRecord, name='clieReserveRecord'),
    path('check_authentication/', views.check_authentication, name='check_authentication'),
    path('dentalLogin/', views.dentalLogin, name='dentalLogin'),
    path('doctor_info/', views.doctor_info, name='doctor_info'),
    path('clinic_info/', views.clinic_info, name='clinic_info'),
    path('client_info/', views.client_info, name='client_info'),

    path('doctor/page/cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
]
