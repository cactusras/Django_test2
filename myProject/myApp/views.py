from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .forms import DoctorForm,ClinicForm,ClientForm,SchedulingForm,WorkingHourForm,ExpertiseForm,ReservationForm,WaitingForm
from django.db.models import Q
from django.db import connection
from django.contrib.auth.decorators import login_required
from .filters import docClinicFilter
from .models import Clinic, Doctor, Doc_Expertise, Expertise, Scheduling, WorkingHour,docClinicSearch,Reservation,Client,Waiting
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

def home(request):
    context={}
    return render(request, "myApp/home.html", context)

def index(request):
    context={}
    return render(request, "myApp/index.html", context)

@login_required
def add_doctor(request):
    if request.method == 'POST':
        doctor_form_data = request.session.get('doctor_form_data')
        expertise_list = request.session.get('expertise_list', [])
        schedule_form_data = request.session.get('schedule_form_data')
        working_hour_list = request.session.get('working_hour_list', [])

        if not (doctor_form_data and expertise_list and schedule_form_data and working_hour_list):
            return redirect('step_one')

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
        return redirect('success')

    return redirect('step_one')

#clinic posting
def add_clinic(request):
    if request.method == 'POST':
        form = ClinicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
    else:
        form = ClinicForm()
    return render(request, 'add_clinic.html', {'form': form})

#client posting
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'successAddedClient.html')
    else:
        form = ClientForm()
    return render(request, 'add_client.html', {'form': form})

#session getters刪除好

#doc scheduling前端處理（因前端要顯示）

def add_Reservation(request):
    if request.user.is_authenticated:
        user_id = request.user.id

        if request.method == 'POST':
            # Retrieve session data
            SchedulingID = request.session.get('SchedulingID', 'NotFound')
            ExpID = request.session.get('ExpertiseID', 'Not Found')
            timeS = request.session.get('StartingTime', 'Not defined')
            timeE = request.session.get('EndTime', 'Unavailable')
            
            if SchedulingID == 'NotFound' or ExpID == 'Not Found' or timeS == 'Not defined' or timeE == 'Unavailable':
                return HttpResponse('Missing scheduling information')

            # Convert string times to datetime objects
            timeS = datetime.strptime(timeS, '%Y-%m-%d %H:%M:%S')
            timeE = datetime.strptime(timeE, '%Y-%m-%d %H:%M:%S')
            
            tStatus = True
            # Fetch the expertise duration
            try:
                expertise = Expertise.objects.get(id=ExpID)
                expertise_duration = timedelta(hours=expertise.time.hour, minutes=expertise.time.minute)
            except Expertise.DoesNotExist:
                return HttpResponse('Expertise not found')

            # Check if the doctor has any reservation during the requested time
            existing_reservations = Reservation.objects.filter(SchedulingID=SchedulingID, time_start__lt=timeS)
            if existing_reservations.exists():
                tStatus = False
                return HttpResponse('Time slot already reserved')
            
            # Check if the doctor is working during the requested time
            scheduling = Scheduling.objects.get(id=SchedulingID)
            day_of_week = timeS.weekday() + 1
            working_hours = WorkingHour.objects.filter(
                scheduling=scheduling,
                day_of_week=timeS.weekday() + 1,  # +1 because WorkingHour.day_of_week is 1-7, not 0-6
                start_time__lte=timeS.time(),
                end_time__gte=(timeS + expertise_duration).time()
            )

            if not working_hours.exists():
                return HttpResponse('Doctor is not working during this time')

            # Determine the tStatus based on the checks above
            # Process the form based on tStatus
            if tStatus:
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
            else:
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


@login_required    
def Doc_uploading(request):
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST, request.FILES, prefix='doctor')
        if doctor_form.is_valid():
            request.session['doctor_form_data'] = doctor_form.cleaned_data
            return redirect('step_two')
    else:
        doctor_form = DoctorForm(prefix='doctor')
    return render(request, 'step_one.html', {'doctor_form': doctor_form})

@login_required
def DocExp_uploading(request):
    if request.method == 'POST':
        doc_expertise_form = ExpertiseForm(request.POST, prefix='expertise')
        if doc_expertise_form.is_valid():
            doc_expertise_list = request.session.get('doc_expertise_list', [])
            doc_expertise_list.append(doc_expertise_form.cleaned_data)
            request.session['expertise_list'] = doc_expertise_list
            return redirect('step_two')
    else:
        expertise_form = ExpertiseForm(prefix='expertise')
    return render(request, 'step_two.html', {'expertise_form': expertise_form})

@login_required
def workingHour_upload(request):
    if request.method == 'POST':
        working_hour_form = WorkingHourForm(request.POST, prefix='working_hour')
        if working_hour_form.is_valid():
            working_hour_list = request.session.get('working_hour_list', [])
            working_hour_list.append(working_hour_form.cleaned_data)
            request.session['working_hour_list'] = working_hour_list
            return redirect('step_three')
    else:
        working_hour_form = WorkingHourForm(prefix='working_hour')
    return render(request, 'step_four.html', {'working_hour_form': working_hour_form})

@login_required
def scheduling_upload(request):
    if request.method == 'POST':
        schedule_form = SchedulingForm(request.POST, prefix='schedule')
        if schedule_form.is_valid():
            request.session['schedule_form_data'] = schedule_form.cleaned_data
            return redirect('step_four')
    else:
        schedule_form = SchedulingForm(prefix='schedule')
    return render(request, 'step_three.html', {'schedule_form': schedule_form})

@login_required
def success(request):
    # Get the clinic associated with the logged-in user
    clinic = Clinic.objects.get(user=request.user)

    # Get all doctors associated with this clinic
    doctors = Doctor.objects.filter(clinic=clinic)
    #診所登入(管理/新增醫師)頁面名稱要=doctor_management.html
    return render(request, 'doctor_management.html', {'doctors': doctors, 'clinic': clinic})

@login_required
def delete_doctor(request, doctor_email):
    # Get the doctor object by email, or return a 404 error if not found
    doctor = get_object_or_404(Doctor, email=doctor_email)

    if request.method == "POST":
        doctor.delete()#the doctors schedule, expertise records are delete as well(because cascade)
        return redirect('doctor_management.html')

    return render(request, 'doctor_management.html', {'doctor': doctor})


#above are the reservation handling 計畫是將前端提交的搜索數據放到session storage中，在js裡處理運算邏輯後再到頁面上顯示，但這裡仍需要去檢查scheduling狀態（是否有人預約）

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
    
    return render(request, 'search_results.html', {
        'filter': filter,
        'doc_final': doc_final,
        'clinic_final': clinic_final
    })
    
#schedule tomeslot(輸入start time end time，每一小時割一次)
def get_time_slots(schedule):
    start_time = schedule.WorkingHour.start_time
    end_time = schedule.WorkingHour.end_time
    time_delta = timedelta(minutes=60)  # Adjust as needed (e.g., 60 for hourly slots)

    time_slots = []
    current_time = start_time
    while current_time < end_time:
      
        weekday = schedule.WorkingHour.day_of_week-1
        time_str = current_time.strftime('%H:%M')
        time_slots.append(f"w{weekday},{time_str}")
        current_time += time_delta

    return time_slots

#clinic 載入頁

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
    context = {
       
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
    }
    return render(request, 'clinic_main.html', context)

#reservation id required
#以下為reservation狀態改變

def reservationStCF(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    # Update the status to "checkin Failed"
    reservation.update_status(1) 
    reservation.save()
    
def reservationStSc(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    # Update the status to "checkin successed"
    reservation.update_status(2) 
    reservation.save()
    
def reservationStIt(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    # Update the status to "in treatment"
    reservation.update_status(3) 
    reservation.save()
    
def reservationStFn(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    # Update the status to "Treatment finished"
    reservation.update_status(4) 
    reservation.save()
    #下次預約
    return render(request,'Next_Reservation.html')
    
def reservationStCbD(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    # Update the status to "cancelled by doc"
    reservation.update_status(5) 
    reservation.save()

#預約此醫生按鈕按下去
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

@login_required
def doctorPage_loading(request):
    #取完doctor reservation
    user = request.user
    doctor = Doctor.objects.filter(user=user)
    schedules = Scheduling.objects.filter(DocID = doctor)
    #status 0,2,3才是真正在預約狀態中
    reservations = Reservation.objects.filter(SchedulingID__in=schedules).filter(status__in=[0, 2, 3])
    #empty 他處已有實現邏輯，之後我抄過來就好
   # Empty = 
    context={
    'reservation_list': [
        {
            'client_name': reservation.ClientID.name,
            'appointment_date': reservation.time_start.date(),
            'appointment_time': reservation.time_start.strftime('%H:%M'),
            'expertise': reservation.expertiseID.name, 
            'status': reservation.get_status_display(),  # Use get_status_display() method
        }
        for reservation in reservations
    ]
        
    }
    
    return render(request, 'doctor_page.html', context)
    
    
def client_loading(request):
    user = request.user
    client = Client.objects.filter(user = user)
    reservations = Reservation.objects.filter(ClientID=user)
    waitings = Waiting.objects.filter(ClientID=user)
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

#預約頁面日期選下去，計算可預約時間
def add_times(time1, time2):
	datetime1 = datetime.combine(datetime.min, time1)
	datetime2 = datetime.combine(datetime.min, time2)
	delta1 = datetime1 - datetime.min
	delta2 = datetime2 - datetime.min
	result_delta = delta1 + delta2
	result_time = (datetime.min + result_delta).time()
	return result_time

def available(request):
	doctor_id = request.GET.get('doctor_id')
	date_str = request.GET.get('date')
	date = datetime.strptime(date_str, '%Y-%m-%d').date()
	week_day=date.weekday()

	expertise_name = request.GET.get('expertise_name')	
	#expertise = next((item for item in expertise_list if item['name'] == expertise_name), None)
	expertise_list = request.session.get('expertise_list', [])
	expertise_time = None
	for expertise in expertise_list:
		if expertise['name'] == expertise_name:
			expertise_time = expertise['time']
			break  # Exit the loop once the expertise is found

	schedules = Scheduling.objects.filter(DoctorID=doctor_id).select_related('WorkingHour')#該醫生的所有行程(之前之後)

	#先取了再說，不管是不是當天
	schedule_list = []
	reservation_list = []
	for schedule in schedules:
		if schedule.end_date >= date.today():#只可能預約今天以後的時間，所以以前的schedule不要加入list
			status_conditions = Q(status=0) | Q(status=2) | Q(status=3)
			schedule_condition = Q(schedule_id=schedule)
			reservation = Reservation.objects.filter(status_conditions & schedule_condition)#今天以後已經被預約走的
           
			for res in reservation:
			    reservation_list.append({
					'scheduleID' : res.SchedulingID,
					'date' :res.time_start.date(),
					'start_time': res.time_start,
					'end_time': res.time_end
				})
       
            schedule_list.append({
                'start_date': schedule.StartDate,
                'end_date': schedule.EndDate,
                'day_of_week': schedule.WorkingHour.day_of_week,
                'start_time': schedule.WorkingHour.start_time,
                'end_time': schedule.WorkingHour.end_time
            })
		
        
			
	time_available = []
	#此時time_available是要預約當日醫生有上班的時段們
	for schedule in schedule_list:
		#選擇預約日期當天無效且工作的日子不對的schedule不會加入
		if schedule['start_date'] <= date and schedule['end_date'] >= date and schedule['day_of_week'] == week_day:
			available = {
				'start_time': schedule['start_time'],
				'end_time': schedule['end_time']
			}
			time_available.append(available)
	#扣掉已經被預約的時段(上班時段包含整個預約時段、預約時段跨開始時間、預約時段跨結束時間)
	for reservation in reservation_list:
		if reservation['date'] == date:#如果已經預約的紀錄，日期跟我想預約的日期相同
			for available in time_available[:]:
				if available['start_time'] <= reservation['start_time'] and available['end_time'] >= reservation['start_time']:#res起始在schedule範圍內
					available['end_time'] = reservation['start_time']
					if available['end_time'] >= reservation['end_time']:
						new_segment = {
							'start_time': reservation['end_time'],
							'end_time': available['end_time']
						}
						time_available.append(new_segment)
					
				if available['end_time'] >= reservation['end_time']:
					available['start_time'] = reservation['end_time']
	#扣完，時段會破碎，所以把連續的時段併在一起	
	time_available = sorted(time_available, key=lambda x: x['start_time'])
	consolidated_time_available = []
	for available in time_available:
		if consolidated_time_available and consolidated_time_available[-1]['end_time'] == available['start_time']:
			consolidated_time_available[-1]['end_time'] = available['end_time']
		else:
			consolidated_time_available.append(available)

	#考量治療時間，修改time_available
	#expertise_time
	reserve_choises = []
	for available in consolidated_time_available:
		start = available['start_time']
		while add_times(start, expertise_time) <= available['end_time']:
			reserve_choises.append(start.strftime('%H:%M:%S'))
			start = add_times(start, expertise_time)

	return JsonResponse({'reserve_choices': reserve_choises})



#login check身份別，django 自帶，用isinstance分身份
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
                    'username': user.username,
                    'email': user.email
                }
                return JsonResponse(response)
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})