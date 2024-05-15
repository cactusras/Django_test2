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
        
        if Docform.is_valid() and Schedform.is_valid() and WHrfrom.is_valid() and Doc_Expform.is_valid():
            
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
            SchedulingID = get_session_SchedulingID(request)
            ExpID = get_session_expID(request)
            timeS = get_session_startT(request)
            timeE = get_session_EndT
            if get_session_timeStatus:
                form = ReservationForm(request.POST)
                if form.is_valid(): 
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO Reservation VALUES(user_id, SchedulinID, ExpID, timeS,timeE,0)")
                else:
                    return HttpResponse('form not valid')
            else: 
                form = WaitingForm(request.POST)
                if form.is_valid(): 
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO Waiting VALUES(user_id, SchedulinID, ExpID, timeS,timeE,False)")
                else:
                    return HttpResponse('form not valid')
            
        #return HttpResponse(f'Your userid is {user_id}')
    else:
        return HttpResponse('Login failed')
    
    
    
    
    

        
        









