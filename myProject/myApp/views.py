from django.shortcuts import render
from django.http import HttpResponse
from .forms import DoctorForm
from .forms import ClinicForm
from .forms import ClientForm
from .forms import SchedulingForm
from .forms import WorkingHourForm
from .forms import Doctor_ExpertiseForm
from .forms import ReservationForm
from .forms import WaitingForm
from django.db import connection

def home(request):
    context={}
    return render(request, "myApp/home.html", context)

def index(request):
    
    context={}
    return render(request, "myApp/index.html", context)



def add_doctor(request):
    if request.method == 'POST':
        Docform = DoctorForm(request.POST, request.FILES)
        Schedform = SchedulingForm(request.POST)
        WHrfrom = WorkingHourForm(request.POST)
        Doc_Expform = Doctor_ExpertiseForm(request.POST)
        
        if Docform.is_valid() and Schedform.is_valid and WHrfrom.is_valid and Doc_Expform.is_valid:
            
            doc_instance = Docform.save()  # 保存 DoctorForm 的實例並獲取對象
            whr_instance = WHrfrom.save(commit=False)  # 保存 WorkingHourForm 的實例但不提交
            sched_instance = Schedform.save(commit=False)  # 保存 SchedulingForm 的實例但不提交
            doc_exp_instance = Doc_Expform.save(commit=False)  # 保存 Doctor_ExpertiseForm 的實例但不提交
            
            # 為其他表單實例設置外鍵關係
            whr_instance.doctor = doc_instance
            sched_instance.doctor = doc_instance
            doc_exp_instance.doctor = doc_instance
            
            whr_instance.save()  # 提交 WorkingHourForm 的實例
            sched_instance.save()  # 提交 SchedulingForm 的實例
            doc_exp_instance.save()  # 提交 Doctor_ExpertiseForm 的實例
            
            return render(request, 'success.html')
    else:
        form = DoctorForm()
    return render(request, 'add_doctor.html', {'form': form})


def add_clinic(request):
    if request.method == 'POST':
        form = ClinicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
    else:
        form = ClinicForm()
    return render(request, 'add_clinic.html', {'form': form})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'successAddedClient.html')
    else:
        form = ClientForm()
    return render(request, 'add_client.html', {'form': form})


def get_session_docRsv(request):
    DocID = request.session.get('DoctorID','Not Found')
    return DocID

def get_session_expID(request):
    ExpID = request.session.get('ExpertiseID','Not Found')
    return ExpID

def get_session_startT(request):
    StartingT = request.seesion.get('StartingTime','Not defined')
    return StartingT


#end Time 前端sessiomStorage計算結果
def get_session_EndT(request):
    EndT = request.session.get('EndTime','Unavailable')
    return EndT

def get_session_timeStatus(request):
    tStatus = request.session.get('TimeStatus','Not found')
    return tStatus

def get_session_SchedulingID(request):
    SchedID = request.session.get('SchedulingID','NotFound')
    return SchedID

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
                expertise_duration = timedelta(hours=expertise.time.hour, minutes=expertise.time.minute)
            except Expertise.DoesNotExist:
                return HttpResponse('Expertise not found')
            #可預約，邏輯參考avaliable
            status_conditions = Q(status=0) | Q(status=2) | Q(status=3)
            reservations = Reservation.objects.filter(
                SchedulingID=SchedulingID,
                time_start__lt=datetime.combine(datetime.strptime(date, '%Y-%m-%d').date(), timeS),
                time_end__gt=datetime.combine(datetime.strptime(date, '%Y-%m-%d').date(), timeS),
                Expertise = expertise
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

        request.session.flush()
        return (request,'myApp/UserAppointmentRecords.html')
    else:
        return HttpResponse('Login failed')
    
    
    
    
    

        
        









