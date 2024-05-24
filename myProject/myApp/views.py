import json
import time
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Clinic, Doctor, Client
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
    return render(request, "searchPage.html", context)

def clieReserve(request):
    context={}
    return render(request, "client_reservation.html", context)

def cliedataEd(request):
    context={}
    return render(request, "client_dataEdit.html", context)

def clinDataEd(request):
    context={}
    return render(request, "clinic_dataEdit.html", context)

def docRegis(request):
    context={}
    return render(request, "doctor_regis.html", context)

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

#add doctor不需要設自動登入
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
            
            whr_instance.save()  # 提交 WForkingHourForm 的實例
            sched_instance.save()  # 提交 SchedulingForm 的實例
            doc_exp_instance.save()  # 提交 Doctor_ExpertiseForm 的實例
            
            return JsonResponse({'Success': 'Doctor registered successfully'})
        else:
            return JsonResponse({'Error': 'Form is not valid'}, status=400)
    else:
        form = DoctorForm()
    return render(request, 'doctor_regis.html', {'form': form})

def add_clinic(request):
    if request.method == 'POST':
        form = ClinicForm(request.POST, request.FILES)
        if form.is_valid():
            clinUser = form.save()
            login(request, clinUser)  
            return JsonResponse({'Success': 'Clinic registered successfully'})
        else:
            return JsonResponse({'Error': 'Form is not valid'}, status=400)
    else:
        form = ClinicForm()
    return render(request, 'clinic_dataEdit.html', {'form': form})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            clieUser = form.save()
            login(request, clieUser)  
            return JsonResponse({'Success': 'Client registered successfully'})
        else:
            return JsonResponse({'Error': 'Form is not valid'}, status=400)
    else:
        form = ClientForm()
    return render(request, 'client_dataEdit.html', {'form': form})


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
                    'username': user.username,
                    'email': user.email
                }

                if user_type == 'Client':
                    return redirect('/searchPage')
                elif user_type == 'Clinic':
                    return redirect('/clinicPage')
                elif user_type == 'Doctor':
                    return redirect('/doctorPage')
                
                # 如果以上所有都不匹配，則返回登錄頁面
                return redirect('/ClicktoEditSchedule')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})