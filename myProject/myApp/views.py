from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .forms import DoctorForm,ClinicForm,ClientForm,SchedulingForm,WorkingHourForm,ExpertiseForm,Doctor_ExpertiseForm,ReservationForm,WaitingForm

from django.db import connection
from django.contrib.auth.decorators import login_required
from .filters import docClinicFilter
from .models import Clinic, Doctor, Doc_Expertise, Expertise, Scheduling, WorkingHour,docClinicSearch,Reservation
from datetime import datetime, timedelta

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

    
#above are the reservation handling 計畫是將前端提交的搜索數據放到session storage中，在js裡處理運算邏輯後再到頁面上顯示，但這裡仍需要去檢查scheduling狀態（是否有人預約）
#use the Fetch API to make an asynchronous POST request to the newly created Django view function.

def doctor_clinic_search_view(request):
    filter = docClinicFilter(request.GET, queryset=docClinicSearch.objects.all())
    return render(request, 'search_results.html', {'filter': filter})



 
        
    

        
        









