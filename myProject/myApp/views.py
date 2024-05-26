import json
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.db import connection
from .forms import (
    DoctorForm, ClinicForm, ClientForm, SchedulingForm,
    WorkingHourForm, ExpertiseForm, ReservationForm, WaitingForm
)
from .filters import docClinicFilter
from .models import (
    Clinic, Doctor, Doc_Expertise, Expertise, Scheduling,
    WorkingHour, docClinicSearch, Reservation, Client, Waiting
)
from django.db.models import Q


def home(request):
    context={}
    return render(request, "searchPage.html", context)

def clieReserve(request):
    context={}
    return render(request, "client_reservation.html", context)

def clinReserve(request):
    context={}
    return render(request, "clinic_reserve.html", context)

def docReserve(request):
    context={}
    return render(request, "doctor_reserve.html", context)

def cliedataEd(request):
    context={}
    return render(request, "client_dataEdit.html", context)

def clinDataEd(request):
    context={}
    return render(request, "clinic_dataEdit.html", context)

def docDataEd(request):
    context={}
    return render(request, "doctor_dataEdit.html", context)

def clickSchedule(request):
    context={}
    return render(request, "ClicktoEditSchedule.html", context)

def login(request):
    context={}
    return render(request, "login.html", context)

def clinHome(request):
    context={}
    return render(request, "clinicPage.html", context)

def docManage(request):
    context={}
    return render(request, "doctor_management.html", context)

def docPage(request):
    context={}
    return render(request, "doctorPage.html", context)

def clieReserveRecord(request):
    context={}
    return render(request, "UserAppointmentRecords.html", context)

def dentalLogin(request):
    context={}
    return render(request, "dentalLogin.html", context)


# 用filter查看所有诊所/醫生/病患的email資料是否已存在
@csrf_exempt
def isUniqueEmail_clin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if Clinic.objects.filter(email=email).exists():
            return JsonResponse({'isUnique': False}, status=200)
        else:
            return JsonResponse({'isUnique': True}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def isUniqueLicense_clin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        license_number = data.get('license_number')
        if Clinic.objects.filter(license_number=license_number).exists():
            return JsonResponse({'isUnique': False}, status=200)
        else:
            return JsonResponse({'isUnique': True}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def isUniqueEmail_clie(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if Client.objects.filter(email=email).exists():
            return JsonResponse({'isUnique': False}, status=200)
        else:
            return JsonResponse({'isUnique': True}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def isUniqueEmail_doc(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if Doctor.objects.filter(email=email).exists():
            return JsonResponse({'isUnique': False}, status=200)
        else:
            return JsonResponse({'isUnique': True}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def add_Reservation(request):
    

    if request.user.is_authenticated:
        user_id = request.user.id

        if request.method == 'POST':
            # Retrieve session data
            doctor_id = request.session.get('doctor_id')
            date = request.session.get('date')  # Assuming date format is YYYY-MM-DD
            
            try:
                scheduling = Scheduling.objects.get(DoctorID=doctor_id, StartDate__lte=date, EndDate__gte=date)
                SchedulingID = scheduling.id
            except Scheduling.DoesNotExist:
                return HttpResponse('No scheduling found for this doctor on selected date')

            ExpID = request.session.get('ExpertiseID', 'Not Found')
            timeS = request.session.get('StartingTime', 'Not defined')

            if SchedulingID == 'NotFound' or ExpID == 'Not Found' or timeS == 'Not defined' :
                return HttpResponse('Missing scheduling information')

            # Convert string times to datetime objects
            timeS = datetime.strptime(timeS, '%Y-%m-%d %H:%M:%S')
            
            # Fetch the expertise duration
            try:
                expertise = Expertise.objects.get(id=ExpID)
                expertise_duration = datetime.timedelta(hours=expertise.time.hour, minutes=expertise.time.minute)
            except Expertise.DoesNotExist:
                return HttpResponse('Expertise not found')
            #可預約，邏輯參考avaliable
            status_conditions = Q(status=0) | Q(status=2) | Q(status=3)
            reservations = Reservation.objects.filter(
                SchedulingID=SchedulingID,
                time_start__lt=datetime.combine(datetime.strptime(date, '%Y-%m-%d').date(), timeS),
                time_end__gt=datetime.combine(datetime.strptime(date, '%Y-%m-%d').date(), timeS),
                Exoertise = expertise
            )
            scheduling = Scheduling.objects.get(id=SchedulingID)
            day_of_week = timeS.weekday() + 1
            working_hours = WorkingHour.objects.filter(
                day_of_week=timeS.weekday() + 1,  # +1 because WorkingHour.day_of_week is 1-7, not 0-6
                start_time__lte=timeS.time(),
                end_time__gte=(timeS + expertise_duration).time()
            )

            if not working_hours.exists():
                return HttpResponse('Doctor is not working during this time')

            status_conditions = Q(status=1) | Q(status=5)
            schedule_condition = Q(schedule_id=SchedulingID)
            if (status_conditions&schedule_condition):
                form = ReservationForm(request.POST)
                if form.is_valid():
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute("INSERT INTO Reservation (ClientID, SchedulingID, expertiseID, time_start, time_end, status) VALUES (%s, %s, %s, %s, %s, %s)",
                                           [user_id, SchedulingID, ExpID, timeS, timeS + expertise_duration, 0])
                        return HttpResponse('Reservation successfully created')
                    except Exception as e:
                        return HttpResponse(f'Error creating reservation: {e}')
                else:
                    return HttpResponse('Form not valid')
            elif schedule_condition:
                form = WaitingForm(request.POST)
                if form.is_valid():
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute("INSERT INTO Waiting (ClientID, SchedulingID, expertiseID, time_start, time_end, is_waiting) VALUES (%s, %s, %s, %s, %s, %s)",
                                           [user_id, SchedulingID, ExpID, timeS, timeS + expertise_duration, False])
                        return HttpResponse('Added to waiting list')
                    except Exception as e:
                        return HttpResponse(f'Error adding to waiting list: {e}')
                else:
                    return HttpResponse('Form not valid')

        return HttpResponse(f'Your user ID is {user_id}')
    else:
        return HttpResponse('Login failed')

#add doctor不需要設自動登入(finished)
def add_doctor(request):
    if request.method == 'POST':
        doctor_form_data = request.session.get('doctor_form_data')
        expertise_list = request.session.get('expertise_list', [])
        schedule_form_data = request.session.get('schedule_form_data')
        working_hour_list = request.session.get('working_hour_list', [])

        if not (doctor_form_data and expertise_list and schedule_form_data and working_hour_list):
            return render(request,'doctor_dataEdit.html')

        clinic = Clinic.objects.get(user=request.user)
        # Add clinic to the doctor form data
        doctor_form_data['clinic'] = clinic

        email = doctor_form_data.pop('email')
        doctor, created = Doctor.objects.update_or_create(email=email, defaults=doctor_form_data)

        # Delete all existing doctor expertise entries
        Doc_Expertise.objects.filter(doctor=doctor).delete()

        # Create new doctor expertise instances
        for expertise_data in expertise_list:
            expertise_name = expertise_data.get('name')
            expertise, created = Expertise.objects.get_or_create(name=expertise_name)
            Doc_Expertise.objects.create(doctor=doctor, expertise=expertise)

        for working_hour_data in working_hour_list:
            working_hour, created = WorkingHour.objects.update_or_create(
                day_of_week=working_hour_data['day_of_week'],
                start_time=working_hour_data['start_time'],
                end_time=working_hour_data['end_time'],
                defaults=working_hour_data
            )
            Scheduling.objects.update_or_create(
                doctor=doctor,
                working_hour=working_hour,
                defaults=schedule_form_data
            )

        request.session.flush()
        return JsonResponse({'success': True}, status=200)

    return render(request,'doctor_dataEdit.html')

def add_clinic(request):
    if request.method == 'POST':
        form = ClinicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'clinic_dataEdit.html')
    else:
        form = ClinicForm()
    return render(request, 'clinic_dataEdit.html', {'form': form})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'searchPage.html')
    else:
        form = ClientForm()
    return render(request, 'client_dataEdit.html', {'form': form})

#判斷使用者是否為登入狀態 
def check_authentication(request):
    if request.user.is_authenticated:
        return JsonResponse({'is_authenticated': True})
    else:
        return JsonResponse({'is_authenticated': False})

#fetch出user的資料(在dataEdit頁面顯示)   
def doctor_info(request):
    if hasattr(request.user, 'doctor'):
        user = request.user
        info = {
            'email': user.email,
            'name': user.name,
            'phone_number': user.phone_number,
            'password': user.pw,
            'photo_url': user.doctor.photo.url,
            'experience': user.doctor.experience,
        }
        return JsonResponse(info)
    else:
        return JsonResponse({'error': 'User is not a doctor'}, status=400)
    
def client_info(request):
    if hasattr(request.user, 'client'):
        user = request.user
        info = {
            'email': user.email,
            'name': user.name,
            'phone_number': user.phone_number,
            'password': user.pw,
            'address': user.client.address,
            'birth_date': user.client.birth_date,
            'gender': user.client.gender,
            'occupation': user.client.occupation,
            'notify': user.client.notify,
        }
        return JsonResponse(info)
    else:
        return JsonResponse({'error': 'User is not a client'}, status=400)

def clinic_info(request):
    if hasattr(request.user, 'clinic'):
        user = request.user
        info = {
            'email': user.email,
            'name': user.name,
            'phone_number': user.phone_number,
            'password': user.pw,
            'photo': user.clinic.photo.url,
            'license_number': user.clinic.license_number,
            'address': user.clinic.address,
            'introduction': user.clinic.introduction,
        }
        return JsonResponse(info)
    else:
        return JsonResponse({'error': 'User is not a clinic admin'}, status=400)
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                user_type = None
                if isinstance(user, Client):
                    user_type = 'Client'
                elif isinstance(user, Clinic):
                    user_type = 'Clinic'
                elif isinstance(user, Doctor):
                    user_type = 'Doctor'

                response = {
                    'status': 'success',
                    'message': 'User is logged in',
                    'user_type': user_type,
                }

                return JsonResponse(response)

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


#醫生的其他資料(new step2)(finished)
@login_required    
def Doc_uploading(request):
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST, request.FILES)
        if doctor_form.is_valid():
            request.session['doctor_form_data'] = doctor_form.cleaned_data
            return render(request,'ClicktoEditSchedule.html')
    else:
        doctor_form = DoctorForm()
    return render(request, 'doctor_dataEdit.html', {'doctor_form': doctor_form})

#(醫生註冊)expertise的確認btn
@login_required
def DocExp_uploading(request):
    if request.method == 'POST':
        doc_expertise_form = ExpertiseForm(request.POST)
        if doc_expertise_form.is_valid():
            doc_expertise_list = request.session.get('doc_expertise_list', [])
            doc_expertise_list.append(doc_expertise_form.cleaned_data)
            request.session['expertise_list'] = doc_expertise_list
            return render(request,'doctor_dataEdit.html')
    else:
        expertise_form = ExpertiseForm()
    return render(request, 'doctor_dataEdit.html', {'expertise_form': expertise_form})

#每次新增時段跳出視窗的新增function(finished)
@login_required
def workingHour_upload(request):
    if request.method == 'POST':
        working_hour_form = WorkingHourForm(request.POST)
        if working_hour_form.is_valid():
            working_hour_list = request.session.get('working_hour_list', [])
            working_hour_list.append(working_hour_form.cleaned_data)
            request.session['working_hour_list'] = working_hour_list
            return render(request,'ClicktoEditSchedule.html')
    else:
        working_hour_form = WorkingHourForm()
    return render(request, 'ClicktoEditSchedule.html', {'working_hour_form': working_hour_form})

#要篩日期大小順序(finished)
@login_required
def scheduling_upload(request):
    if request.method == 'POST':
        scheduling_form = SchedulingForm(request.POST)
        if scheduling_form.is_valid():
            request.session['schedule_form_data'] = scheduling_form.cleaned_data
            return render(request,'doctor_dataEdit.html')
    else:
        schedule_form = SchedulingForm()
    return render(request, 'ClicktoEditSchedule.html', {'scheduling_form': scheduling_form})

#(finished)
@login_required
def success(request):
    # Get the clinic associated with the logged-in user
    clinic = Clinic.objects.get(user=request.user)

    # Get all doctors associated with this clinic
    doctors = Doctor.objects.filter(clinic=clinic)
    #診所登入(管理/新增醫師)頁面名稱要=doctor_management.html
    return render(request, 'doctor_management.html', {'doctors': doctors, 'clinic': clinic})

#(finished)
@login_required
def delete_doctor(request, doctor_email):
    # Get the doctor object by email, or return a 404 error if not found
    doctor = get_object_or_404(Doctor, email=doctor_email)

    if request.method == "POST":
        doctor.delete()#the doctors schedule, expertise records are delete as well(because cascade)
        return redirect('doctor_management.html')

    return render(request, 'doctor_management.html', {'doctor': doctor})

def doctor_clinic_search_view(request):
        # Apply the filter
    filter = docClinicFilter(request.GET, queryset=docClinicSearch.objects.all())

    # Retrieve detailed information for each filtered doctor
    detailed_doctors = []
    detailed_clinics = []
    for result in filter.qs:
        doctor_details = {
            'doc_id': result.doc_id,
            'doc_name': result.doc_name,  # Changed from result.name to result.doc_name
            'clinic_name': result.clinic_name,
            'clinic_adress': result.clinic_adress,
            'doc_exp': result.exp_name
        }
        detailed_doctors.append(doctor_details)

        clinic_details = {
            'clinic_id': result.clinic_id,
            'clinic_name': result.clinic_name,
            'clinic_adress': result.clinic_adress,
            'clinic_introduction': result.clinic_introduction,
            'doc_exp': result.exp_name
        }
        detailed_clinics.append(clinic_details)  # Changed from detailed_doctors to detailed_clinics

    # Combine doctor details
    doc_final = []
    for doc in detailed_doctors:
        # Check if the doctor already exists in doc_final
        existing_doctor = next((item for item in doc_final if item['doc_name'] == doc['doc_name']), None)
        if existing_doctor:
            # Append the expertise to the existing doctor's expertise list
            existing_doctor['doc_exp'].append(doc['doc_exp'])
        else:
            # Create a new dictionary for the doctor
            new_doctor = {
	    'doc_id': doc['doc_id'],
                'doc_name': doc['doc_name'],
                'clinic_name': doc['clinic_name'],
                'clinic_adress': doc['clinic_adress'],
                'doc_exp': [doc['doc_exp']]  # Initialize doc_exp as a list
            }
            doc_final.append(new_doctor)

            # Update session with doctor IDs
            #doc_list = request.session.get('doc_list', [])
            #doc_list.append(doc['doc_id'])
            #request.session['doc_list'] = doc_list  # Save session

    # Combine clinic details
    clinic_final = []
    for clinic in detailed_clinics:
        # Check if the clinic already exists in clinic_final
        existing_clinic = next((item for item in clinic_final if item['clinic_name'] == clinic['clinic_name']), None)
        if existing_clinic:
            # Append the expertise to the existing clinic's expertise list
            existing_clinic['doc_exp'].append(clinic['doc_exp'])
        else:
            # Create a new dictionary for the clinic
            new_clinic = {
	    'clinic_id': clinic['clinic_id'],
                'clinic_name': clinic['clinic_name'],
                'clinic_adress': clinic['clinic_adress'],
                'clinic_introduction': clinic['clinic_introduction'],
                'doc_exp': [clinic['doc_exp']]  # Initialize doc_exp as a list
            }
            clinic_final.append(new_clinic)

            # Update session with clinic IDs
            #clinic_list = request.session.get('clinic_list', [])
            #clinic_list.append(clinic['clinic_id'])
            #request.session['clinic_list'] = clinic_list  # Save session
    
    return render(request, 'searchPage.html', {
        'filter': filter,
        'doc_final': doc_final,
        'clinic_final': clinic_final
    })
    
#schedule timeslot(輸入start time end time，每一小時割一次)
def get_time_slots(schedule):
    start_time = schedule.WorkingHour.start_time
    end_time = schedule.WorkingHour.end_time
    time_delta = datetime.timedelta(minutes=60)  # Adjust as needed (e.g., 60 for hourly slots)

    time_slots = []
    current_time = start_time
    while current_time < end_time:
      
        weekday = schedule.WorkingHour.day_of_week-1
        time_str = current_time.strftime('%H:%M')
        time_slots.append(f"w{weekday},{time_str}")
        current_time += time_delta

    return time_slots

#clinic 載入頁(finished)
@login_required
def clinic_load(request):
    #return clinic main page
    user = request.user
    clinics = Clinic.objects.filter(user=user)
    #診所
    
    #sched field
    #DoctorID = models.ForeignKey('Doctor', related_name='scheduling', on_delete=models.CASCADE)
    #WorkingHour = models.ForeignKey('WorkingHour', related_name='scheduling', on_delete=models.CASCADE)
    #StartDate = models.DateField()
    #EndDate = models.DateField()
    
    schedules = Scheduling.objects.filter(clinic=clinics)
    #注意回傳值
    reservations = Reservation.objects.filter(schedulesID = schedules)
    reservation_list = [
        {
            'client_name': reservation.ClientID.name,
            'appointment_date': reservation.time_start.date(),
            'appointment_time': reservation.time_start.strftime('%H:%M'),
            'expertise': reservation.expertiseID.name,  # 假设 Expertise 有一个 'name' 字段
            'status': reservation.get_status_display(),  # 使用 get_status_display() 方法获取状态显示
        }
        for reservation in reservations
    ]
    '''context = {
       
    'clinic': clinics,
    'schedules': schedules,
    'reservations': reservations,
    # Additional context variables:
    'clinic_name': clinics[0].name,  # Assuming clinics is a list with a single clinic=?
    #return w1,10:00=>11, w1 11:00=>12...so on
    'schedule_list': [
        {
            'doctor_name': schedule.DoctorID.name,
            'time_slots': get_time_slots(schedule),
        }
        for schedule in schedules
    ],
    
    'reservation_list': [
        {
            'client_name': reservation.ClientID.name,
            'appointment_date': reservation.time_start.date(),
            'appointment_time': reservation.time_start.strftime('%H:%M'),
            'expertise': reservation.expertiseID.name,  # Assuming Expertise has a 'name' field
            'status': reservation.get_status_display(),  # Use get_status_display() method
        }
        for reservation in reservations
    ],
    }'''
    return render(request, 'clinicPage.html', {'reservation_list': reservation_list})

#reservation id required
#以下為reservation狀態改變

def reservationStCF(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    # Update the status to "checkin Failed"
    reservation.update_status(1) 
    reservation.save()
    return render(request,'clinicPage.html')
    
def reservationStSc(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    # Update the status to "checkin successed"
    reservation.update_status(2) 
    reservation.save()
    return render(request,'clinicPage.html')
    
def reservationStIt(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    # Update the status to "in treatment"
    reservation.update_status(3) 
    reservation.save()
    return render(request,'clinicPage.html')
    
def reservationStFn(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    # Update the status to "Treatment finished"
    reservation.update_status(4) 
    reservation.save()
    #下次預約
    return render(request,'clinicPage.html')
    
    
def reservationStCbD(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    # Update the status to "cancelled by doc"
    reservation.update_status(5) 
    reservation.save()
    return render(request,'clinicPage.html')

#預約此醫生按鈕按下去
def doctor_reserve_page(request, doc_id):

	request.session['doc_id'] = doc_id  # Save session

	# Fetch the doctor based on doc_id
	doctor = get_object_or_404(Doctor, id=doc_id)
	clinic = get_object_or_404(Clinic, id=doctor.clinicID)

	# Fetch the expertise related to the doctor
	doctor_expertise = Doc_Expertise.objects.filter(DocID=doctor).select_related('Expertise_ID')

	# Create a list of dictionaries with expertise name and time
	expertise_list = []
	for expertise in doctor_expertise:
		expertise_dict = {
			'name': expertise.Expertise_ID.name,
			'time': expertise.Expertise_ID.time
		}
		expertise_list.append(expertise_dict)

	# Store the expertise list in the session
	request.session['expertise_list'] = expertise_list

	context = {
		'doctor': doctor,
		'clinic': clinic,
		'doctor_expertise': expertise_list,
		#'schedules': doc_schedule_list
		#'reserved': reservation_list
	}
	return render(request, 'doctor_reserve.html', context)

#診所預約按鈕按下去
def clinic_reserve_page(request, clinic_id):
    
    clinic_details = get_object_or_404(Clinic, id='clinic_id')
    return render(request, 'clinic_reserve.html', clinic_details)

#(finished)
@login_required
def doctorPage_loading(request):
    #取完doctor reservation
    user = request.user
    doctor = Doctor.objects.filter(id=user.id)
    
    schedules = Scheduling.objects.filter(DocID = doctor.id)
    #status 0,2,3才是真正在預約狀態中
    reservations = Reservation.objects.filter(SchedulingID__in=schedules).filter(status__in=[0, 2, 3])
    empty_list = Reservation.objects.filter(SchedulingID__in=schedules).filter(status__in=[1, 5])
    #是不是有另一種寫法？
    #empty 他處已有實現邏輯，之後我抄過來就好
    
    #context={
    reservation_list = [
        {
            'client_name': reservation.ClientID.name,
            'appointment_date': reservation.time_start.date(),
            'appointment_time': reservation.time_start.strftime('%H:%M'),
            'expertise': reservation.expertiseID.name, 
            'status': reservation.get_status_display(),  # Use get_status_display() method
        }
        for reservation in reservations
    ]
    
        
    #}
    
    return render(request, 'doctorPage.html', reservation_list)
        
def clientRecord_loading(request):
    user = request.user
    client = Client.objects.filter(id = user.id)
    reservations = Reservation.objects.filter(ClientID=client.id)
    waitings = Waiting.objects.filter(ClientID=client.id)
    context ={
        'reservation_list': [
        {
            'client_name': reservation.ClientID.name,
            'appointment_date': reservation.time_start.date(),
            'appointment_time': reservation.time_start.strftime('%H:%M'),
            'expertise': reservation.expertiseID.name, 
            'status': reservation.get_status_display(),  # Use get_status_display() method
        }
        for reservation in reservations
        ],
         'waiting_list': [
        {
            'client_name': waiting.ClientID.name,
            'appointment_date': waiting.time_start.date(),
            'appointment_time': waiting.time_start.strftime('%H:%M'),
            'expertise': waiting.expertiseID.name, 
            'status': waiting.get_status_display(),  # Use get_status_display() method
        }
        for waiting in waitings
        ],
         
         
    }
    return render(request,'UserAppointmentRecords.html',context)

#如果是Status = 2或3的話 就不執行而是跳jsonresponse
#變數名有待確認
def client_cancel_reservation(request):

    if request.method == 'GET':
        reserveID = request.GET.get('reservationID')
        reservation = get_object_or_404(Reservation, reservationID=reserveID)

        if (reservation.Status == 2 or reservation.Status == 3):
            return JsonResponse() #不能取消
        else:
            return JsonResponse() #可以取消
        
        # 删除预约
        reservation.delete()
        
    
    return render(request, 'UserAppointmentRecords.html')


#預約頁面日期選下去，計算可預約時間

def add_times(time1, duration):
    # Helper function to add a timedelta to a time object
    datetime1 = datetime.combine(datetime.min, time1)
    result_datetime = datetime1 + duration
    return result_datetime.time()

def available(request):
    # Get doctor_id, date, and expertise_name from the GET request
    doctor_id = request.GET.get('doctor_id')
    date_str = request.GET.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    week_day = date.weekday()


    expertise_name = request.GET.get('expertise_name')
    expertise_list = request.session.get('expertise_list', [])
    expertise_time = None
   
    # Find the expertise time from the session
    for expertise in expertise_list:
        if expertise['name'] == expertise_name:
            expertise_time = datetime.strptime(expertise['time'], '%H:%M:%S').time()
            break  # Exit the loop once the expertise is found


    # Fetch all schedules for the given doctor, including related WorkingHour data
    schedules = Scheduling.objects.filter(DoctorID=doctor_id).select_related('WorkingHour')


    schedule_list = []
    reservation_list = []
   
    # Filter and prepare the schedule list
    for schedule in schedules:
        if schedule.EndDate >= date.today():  # Only include future schedules
            status_conditions = Q(status=0) | Q(status=2) | Q(status=3)
            schedule_condition = Q(schedule_id=schedule.id)
            reservations = Reservation.objects.filter(status_conditions & schedule_condition)


            # Append schedule details to the schedule list
            schedule_list.append({
                'start_date': schedule.StartDate,
                'end_date': schedule.EndDate,
                'day_of_week': schedule.WorkingHour.day_of_week,
                'start_time': schedule.WorkingHour.start_time,
                'end_time': schedule.WorkingHour.end_time
            })


            # Append reservation details to the reservation list
            for res in reservations:
                reservation_list.append({
                    'scheduleID': res.schedule_id,
                    'date': res.time_start.date(),
                    'start_time': res.time_start,
                    'end_time': res.time_end
                })


    time_available = []
   
    # Filter schedules for the given date
    for schedule in schedule_list:
        if schedule['start_date'] <= date <= schedule['end_date'] and schedule['day_of_week'] == week_day:
            available = {
                'start_time': schedule['start_time'],
                'end_time': schedule['end_time']
            }
            time_available.append(available)


    # Remove reserved times from available times
    for reservation in reservation_list:
        if reservation['date'] == date:
            for available in time_available[:]:
                if available['start_time'] <= reservation['start_time'] < available['end_time']:
                    last_available_end = available['end_time']
                    available['end_time'] = reservation['start_time']
                    if last_available_end >= reservation['end_time']:
                        new_segment = {
                            'start_time': reservation['end_time'],
                            'end_time': last_available_end
                        }
                        time_available.append(new_segment)
                if available['end_time'] >= reservation['end_time'] > available['start_time']:
                    available['start_time'] = reservation['end_time']


    # Consolidate adjacent time slots
    time_available = sorted(time_available, key=lambda x: x['start_time'])
    consolidated_time_available = []
    for available in time_available:
        if consolidated_time_available and consolidated_time_available[-1]['end_time'] == available['start_time']:
            consolidated_time_available[-1]['end_time'] = available['end_time']
        else:
            consolidated_time_available.append(available)


    # Consider expertise time to modify time_available
    reserve_choices = []
    expertise_duration = datetime.timedelta(hours=expertise_time.hour, minutes=expertise_time.minute, seconds=expertise_time.second)
    for available in consolidated_time_available:
        start = available['start_time']
        while add_times(start, expertise_duration) <= available['end_time']:
            reserve_choices.append(start.strftime('%H:%M'))
            start = add_times(start, expertise_duration)


    # Return available reservation choices as a JSON response
    return JsonResponse({'reserve_choices': reserve_choices})

#login check身份別，django 自帶，用isinstance分身份


#存疑，（應該）現在這邊必須要候補時段跟被取消的預約時段一模一樣才卡的進去
@login_required
def waitingToResForC(request):
    user = request.user
    # Find the waiting entries for the current user with status=False
    waiting_list = Waiting.objects.filter(ClientID=user.id, status=False)
    
    # Process and format the waiting list data
    waiting_list_data = []
    for entry in waiting_list:
        # Check if the scheduling slot is available (not reserved)
        if not Reservation.objects.filter(SchedulingID=entry.SchedulingID, Status__in=[0,2,4]).exists():
            # Update the waiting status to True
            entry.status = True
            entry.save()
            # Format the waiting list data
            client_name = entry.ClientID.name
            expertise_name = entry.expertiseID.name
            time_start = entry.time_start.strftime('%Y-%m-%d %H:%M:%S')
            time_end = entry.time_end.strftime('%Y-%m-%d %H:%M:%S')
            waiting_list_data.append({
                'client_name': client_name,
                'expertise_name': expertise_name,
                'time_start': time_start,
                'time_end': time_end
            })
            
              # Insert a new reservation
            reservation = Reservation.objects.create(
                ClientID=entry.ClientID,
                SchedulingID=entry.SchedulingID,
                expertiseID=entry.expertiseID,
                time_start=entry.time_start,
                time_end=entry.time_end,
                Status=0,  # Initial status
            )
            reservation.save()
            
    
    # Return the formatted waiting list data as JSON
    return JsonResponse({'waiting_list': waiting_list_data})