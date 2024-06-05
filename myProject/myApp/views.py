import json, simplejson
import os
from pathlib import Path
from PIL import Image
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
#from rest_framework import serializers
from myProject.encoder import CustomEncoder
from .forms import ClientUpdateForm, ClinicUpdateForm, DoctorForm,ClinicForm,ClientForm, LoginForm,SchedulingForm,WorkingHourForm,ExpertiseForm,ReservationForm,WaitingForm
from django.db.models import Q
from django.db import connection
from django.contrib.auth.decorators import login_required
from .filters import docClinicFilter
from .models import Clinic, Doctor, Doc_Expertise, Expertise, Scheduling, WorkingHour,docClinicSearch,Reservation,Client,Waiting,CustomUser
from datetime import datetime, timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from myApp import forms
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password


def index(request):
    
    context={}
    return render(request, "myApp/index.html", context)

#login check身份別，django 自帶，用isinstance分身份，此處等migrate完可進行初步測試，看要手動加資料還是把register頁面都弄好一併測試（需要頁面跳轉邏輯）
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                username = user.name
                user_type = None

                login(request, user)  # Ensure the user object is passed correctly
                # 登入成功，根據用戶身份導向不同的頁面
                if hasattr(user, 'client'):  # 检查是否是客户
                    print('client')
                    user_type = 'client'
                    return JsonResponse({'user_type': 'client', 'username': username,  'status': 'success'})
                elif hasattr(user, 'clinic'):  # 检查是否是诊所
                    print('clinic')              
                    user_type = 'clinic'
                    return JsonResponse({'user_type': 'clinic', 'username': username,  'status': 'success'})
                elif hasattr(user, 'doctor'):  # 检查是否是医生
                    print('doctor')
                    user_type = 'doctor'
                    return JsonResponse({'user_type': 'doctor', 'username': username,  'status': 'success'})

def add_client(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 解析 JSON 數據
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON', 'status': 'error'})
        
        password = data.get('password')
        email = data.get('email')
        # 創建一個包含數據的 QueryDict
        data = {
            'email': email,
            'name': data.get('name'),
            'phone_number': data.get('phone_number'),
            'password': password,
            'address': data.get('address'),
            'birth_date': data.get('birth_date'),
            'gender': data.get('gender'),
            'occupation': data.get('occupation'),
            'notify': data.get('notify')
        }
        print('password here = ', password)
        try:
            client = Client.objects.get(email=email)
        except Client.DoesNotExist:
            client = None
        print('data = ', data)
        if client:
            form = ClientUpdateForm(data, instance=client)
        else:
            form = ClientForm(data)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            cleaned_data['is_active'] = True
            cleaned_data['is_admin'] = False

            email = cleaned_data.get('email')

            client, created_client = Client.objects.update_or_create(
                email=email,
                defaults=cleaned_data
            )

            if password != '':
                client.password = make_password(data['password'])
                client.save()

            if created_client:
                message = 'Client created successfully.'
            else:
                message = "Client updated successfully."

            return JsonResponse({'message': message, 'status': 'success'})
        else:
            print('error = ', form.errors)
            return JsonResponse({'message': 'Invalid form data', 'errors': form.errors, 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


@login_required
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
    
#clinic posting
def add_clinic(request):
    if request.method == 'POST':
        try:
            # 檢查用戶是否存在
            email = request.POST.get('email')
            if email:
                try:
                    clinic = Clinic.objects.get(email=email)
                    update_clinic = True  # 更新現有診所
                except Clinic.DoesNotExist:
                    update_clinic = False  # 新建診所
            else:
                update_clinic = False
            print('type = ', type(clinic))
            if update_clinic:
                form = ClinicUpdateForm(request.POST, instance=clinic)
            else:
                form = ClinicForm(request.POST, request.FILES)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                print(cleaned_data)
                cleaned_data['is_active'] = True
                cleaned_data['is_admin'] = False
                #如果為資料更新則不進入此判斷
                if 'photo' in cleaned_data:
                    #(註冊時)如果有選擇加照片
                    if cleaned_data['photo'] is not None:
                        # photo = cleaned_data.pop('photo')
                        photo = cleaned_data['photo']
                        image = Image.open(photo)
                        print("photo opend")
                        # Define the save path using Path from pathlib
                        save_dir = Path('media/uploaded_files')
                        save_dir.mkdir(parents=True, exist_ok=True)  # Create directories if they don't exist
                        save_path = save_dir / photo.name
                        image.save(save_path)
                        print("photo saved")
                        photo_path = f'uploaded_files/{photo.name}'
                        cleaned_data['photo'] = photo_path
                        print("photo path saved to clean_data")

                # Prepare data for update_or_create
                email = cleaned_data.pop('email')
                clinic, created_clinic = Clinic.objects.update_or_create(
                    email=email,
                    defaults=cleaned_data
                )

                if 'password' in cleaned_data:
                    clinic.password = make_password(cleaned_data['password'])
                    clinic.save()

                if created_clinic:
                    message = 'Clinic created successfully.'
                else:
                    message = 'Clinic updated successfully.'

                return JsonResponse({'message': message, 'status': 'success'})
            else:
                return JsonResponse({'message': 'Invalid form data', 'errors': form.errors, 'status': 'error'})
        except json.JSONDecodeError:
            return JsonResponse({'message': '無效的 JSON', 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})

#先將加入圖片放在這裡 但可能還有東西要改
@login_required
def add_doctor(request):
    print('add doctor')
    if request.method == 'POST':
        print('add doctor_post yes')
        doctor_form_data = request.session.get('doctor_form_data')
        expertise_list = request.session.get('doc_expertise_list', [])
        schedule_form_data = request.session.get('schedule_form_data')
        working_hour_list = request.session.get('working_hour_list', [])

        print('doc_info = ', doctor_form_data , '  exp_info = ', expertise_list, '  working_hours = ', working_hour_list, '  schedule = ', schedule_form_data)

        '''if not (doctor_form_data and expertise_list and schedule_form_data and working_hour_list):
            return JsonResponse({'message': 'Session data incomplete', 'status': 'error'})'''
        
        if not (doctor_form_data and expertise_list and schedule_form_data):
            return JsonResponse({'message': 'Session data incomplete', 'status': 'error'})

        # Process photo if included in doctor_form_data
        if doctor_form_data['photo'] is not None:
            photo_url = doctor_form_data.pop('photo', '')  # Remove photo from form data
            try:
                save_dir = Path('media/uploaded_files')
                save_dir.mkdir(parents=True, exist_ok=True)
                final_path = save_dir / Path(photo_url).name
                os.rename(photo_url, final_path)
                print("Photo saved successfully")
                doctor_form_data['photo'] = photo_url  # Update form data with saved photo path
            except Exception as e:
                print(f"Error saving photo: {e}")
                return JsonResponse({'message': 'Error saving photo', 'status': 'error'})

        clinic = Clinic.objects.get(id=request.user.id)
        doctor_form_data['clinicID'] = clinic
        email = doctor_form_data.pop('email')
        doctor, created = Doctor.objects.update_or_create(email=email, defaults=doctor_form_data)
        
        Doc_Expertise.objects.filter(DocID=doctor).delete()
        
        for expertise_data in expertise_list:
            expertise_name = expertise_data.get('name')
            expertise, created = Expertise.objects.get_or_create(name=expertise_name)
            Doc_Expertise.objects.create(DocID=doctor, Expertise_ID=expertise)
        
        for working_hour_data in working_hour_list:
            working_hour, created = WorkingHour.objects.update_or_create(
                day_of_week=working_hour_data['day_of_week'],
                start_time=working_hour_data['start_time'],
                end_time=working_hour_data['end_time'],
                defaults=working_hour_data
            )
            Scheduling.objects.update_or_create(
                DoctorID=doctor.id,
                #WorkingHour=1,
                #WorkingHour=working_hour,
                defaults=schedule_form_data
            )

        # Clear session data after successful processing
        request.session.flush()
        return JsonResponse({'message': 'Doctor added successfully', 'status': 'success'})

    return JsonResponse({'message': 'Invalid request method', 'status': 'error'})

def handle_uploaded_file(file):
    save_dir = Path('media/temp_files')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / file.name
    with open(save_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return str(save_path)

@login_required    
def Doc_uploading(request):
    if request.method == 'POST':
        try:
            doctor_form = DoctorForm(request.POST, request.FILES)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON', 'status': 'error'})
        if doctor_form.is_valid():
            clean = doctor_form.cleaned_data
            clean['password'] = make_password(clean['password'])
            photo = request.FILES.get('photo')
            if photo is not None:
                photo_url = handle_uploaded_file(photo)
                clean['photo'] = photo_url
            request.session['doctor_form_data'] = clean
            print('succeed adding', clean)
            doc_expertise_list = request.session.get('doc_expertise_list', None)
            return JsonResponse({'message': 'Doctor Session added', 'status': 'success'})
        else:
            print('error : ', doctor_form.errors)
            return JsonResponse({'message': 'Invalid form data', 'errors': doctor_form.errors, 'status': 'error'})
    else:
        doctor_form = DoctorForm()
    return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


@login_required
def DocExp_uploading(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 解析 JSON 数据
            expertise = data.get('expertise')  # 获取 expertise 值
            doc_expertise_form = ExpertiseForm({'name': expertise})
            
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON', 'status': 'error'})

        if doc_expertise_form.is_valid():
            doc_expertise_list = request.session.get('doc_expertise_list', [])
            doc_expertise_list.append(doc_expertise_form.cleaned_data)
            print("clean = ", doc_expertise_list)
            request.session['doc_expertise_list'] = doc_expertise_list  # 更新 session
            return JsonResponse({'message': 'Expertise data added successfully', 'status': 'success', 'exp': doc_expertise_form.cleaned_data})
        else:
            return JsonResponse({'message': 'Invalid form data', 'errors': doc_expertise_form.errors, 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})

@login_required
def workingHour_upload(request):
    if request.method == 'POST':
        try:
            data_string = request.body.decode('utf-8')
            data = json.loads(data_string)  # 解析 JSON 数据
            print('post succeed')
        except json.JSONDecodeError:
            print('post failed')
            return JsonResponse({'message': 'Invalid JSON', 'status': 'error'})
        start_time_str = data['start_time'] #type(start_time_str) == str
        '''end_time_str = data.get('end_time')
        

        data = {
            'day_of_week' : data.get('day_of_week'),
            'start_time' : start_time_str,
            'end_time' : end_time_str
            #'start_time' : start_time_str.strftime('%H:%M'),
            #'end_time' : end_time_str.strftime('%H:%M')
        }'''
        print('sttime = ', start_time_str) 
        #working_hour_form = WorkingHourForm(data)
        print('before valid')
        #取代form來驗證input的資料型態(連到serializers.py)
        serializer = WorkingHourSerializer(data=data)
        if serializer.is_valid():
            print('after valid1')
            working_hour_list = request.session.get('working_hour_list', [])
            print('first get list = ', working_hour_list)
            # 添加新工作時間到列表中
            working_hour_list.append(serializer.validated_data)
            print('succeed adding', working_hour_list)
            # 將工作時間列表保存回 session
            request.session['working_hour_list'] = working_hour_list
            print('finish')

            #working_hour_list = request.session.get('working_hour_list', [])
            
            #working_hour_list.append(working_hour_form.cleaned_data)
            #working_hour_list.append(data)
            
            # 序列化 time 对象为字符串
            '''workingHour_data = []
            for item in working_hour_list:
                if(type(item['start_time']) == datetime):
                    print('type is datatimeS')
                    item['start_time'] = item['start_time'].strftime('%H:%M')
                if(type(item['end_time']) == datetime):
                    print('type is datatimeE')
                    item['end_time'] = item['end_time'].strftime('%H:%M')
                workingHour_data.append(item)'''
            
            #request.session['working_hour_list'] = working_hour_list
            #print('after valid3')
            #想除掉not serializable的bug 所以寫了這個(跟encoder.py) 但會導到cls的bug
            #serialized_data  = simplejson.dumps(working_hour_list, cls=CustomEncoder)
            #return JsonResponse({'message': 'Working hour data added successfully', 'status': 'success'})
            return HttpResponse(status=204) #我想說改用http看看 但還是有bug 也可能是我json沒有接收好httpresponse? 我不確定
        else:
            print('notvalid = ', serializer.errors)
            #return JsonResponse({'message': 'Invalid form data', 'status': 'error'})
            return HttpResponse('Invalid form data', status=400)
    else:
        working_hour_form = WorkingHourForm()
    
    #return JsonResponse({'message': 'Invalid request method', 'status': 'error'})
    return HttpResponse('Invalid request method', status=405)

'''render版的workingHour_upload 對應到clicktoEditSchedule_new
@login_required
def workingHour_upload(request):
    print('hi')
    if request.method == 'POST':
        print('post here')
        working_hour_form = WorkingHourForm(request.POST)
        print('form = ', working_hour_form)
        if working_hour_form.is_valid():
            print('valid here')
            working_hour_list = request.session.get('working_hour_list', [])
            working_hour_list.append(working_hour_form.cleaned_data)
            request.session['working_hour_list'] = working_hour_list
            print('working = ', working_hour_list)
            return render(request,'myApp/ClicktoEditSchedule.html')
        else:
            print(working_hour_form.errors)
    else:
        working_hour_form = WorkingHourForm()
    
    return JsonResponse({'message': 'Invalid request method', 'status': 'error'})'''


def scheduling_upload(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 解析 JSON 数据        
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON', 'status': 'error'})

        data = {
                'StartDate' : data.get('StartDate'),
                'EndDate' : data.get('EndDate')
            }

        schedule_form = SchedulingForm(data)
        
        if schedule_form.is_valid():
            scheduling_data = schedule_form.cleaned_data
             # 序列化 date 对象为字符串
            scheduling_data['StartDate'] = data.get('StartDate')
            scheduling_data['EndDate'] = data.get('EndDate')
        
            request.session['schedule_form_data'] = scheduling_data
            return JsonResponse({'message': 'Scheduling data added successfully', 'status': 'success'})
        else:
            print('notvalid = ', schedule_form.errors)
            return JsonResponse({'message': 'Invalid form data', 'errors': schedule_form.errors, 'status': 'error'})
    else:
        schedule_form = SchedulingForm()
    
    return JsonResponse({'message': 'Invalid request method', 'status': 'error'})

def doc_session(request):
    print('doc_session')

    # 从会话中获取所需的数据
    doctor_form_data = request.session.get('doctor_form_data', {})
    expertise_list = request.session.get('expertise_list', [])
    schedule_form_data = request.session.get('schedule_form_data', {})
    working_hour_list = request.session.get('working_hour_list', [])
    print('doctor_form = ', doctor_form_data)
    # 构建响应数据
    response_data = {
        'doctor_form_data': doctor_form_data,
        'expertise_list': expertise_list,
        'schedule_form_data': schedule_form_data,
        'working_hour_list': working_hour_list,
    }

    # 返回 JSON 响应
    return JsonResponse(response_data, status=200)

#doctor_management中要抓此診所所有醫生的資料(這樣login_required要刪掉)
@login_required
def success(request):
    clinic = Clinic.objects.get(id=request.user.id)
    doctors = Doctor.objects.filter(clinicID=clinic).values()  # QuerySet 转为字典列表

    data = {
        'clinic': {
            'id': clinic.id,
            'name': clinic.name,
            'phone_number': clinic.phone_number,
            'address': clinic.address,
            'introduction':clinic.introduction
            # 添加其他需要的字段
        },
        'doctors': list(doctors),  # 将 QuerySet 转为列表
    }

    return JsonResponse(data)

@login_required
def delete_doctor(request, doctor_email):
    doctor = get_object_or_404(Doctor, email=doctor_email)

    if request.method == "POST":
        doctor.delete()
        return JsonResponse({'message': 'Doctor deleted successfully', 'status': 'success'})

    return JsonResponse({'message': 'Invalid request method', 'status': 'error'})

@csrf_exempt
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

    # Prepare data to be returned as JsonResponse
    data = {
        'doctors': doc_final,
        'clinics': clinic_final,
    }

    return JsonResponse(data)
    
#schedule tomeslot(輸入start time end time，每一小時割一次)
def get_time_slots(schedule):
    start_time = schedule.WorkingHour.start_time
    end_time = schedule.WorkingHour.end_time
    time_delta = timedelta(minutes=60)  # Adjust as needed (e.g., 60 for hourly slots)

    time_slots = []
    # Convert time to datetime for arithmetic operations
    current_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)

    while current_datetime < end_datetime:
      
        weekday = schedule.WorkingHour.day_of_week-1
        time_str = current_datetime.strftime('%H:%M')
        time_slots.append(f"w{weekday},{time_str}")
        current_datetime += time_delta
    return time_slots

#clinic 載入頁
@login_required
def clinic_load(request):
    user = request.user
    clinic = Clinic.objects.get(id=user.id)
    doctors = Doctor.objects.filter(clinicID=user.id)
    schedules = Scheduling.objects.filter(DoctorID__in=doctors)
    reservations = Reservation.objects.filter(SchedulingID__in=schedules)

    # Build the context as a dictionary
    context = {
        'clinic': {
            'id': clinic.id,
            'name': clinic.name,
            'address': clinic.address,
            'phone_number': clinic.phone_number,
            'email': clinic.email,
        },
        'schedules': [
            {
                'id': schedule.id,
                'doctor_name': schedule.DoctorID.name,
                'start_date': datetime.combine(schedule.StartDate, datetime.min.time()).strftime('%Y-%m-%d'),
                'end_date': datetime.combine(schedule.EndDate, datetime.min.time()).strftime('%Y-%m-%d'),
                'time_slots': get_time_slots(schedule),
            }
            for schedule in schedules
        ],
        'reservations': [
            {
                'id': reservation.id,
                'client_name': reservation.ClientID.name,
                'appointment_date': reservation.time_start.strftime('%Y-%m-%d'),
                'appointment_time': reservation.time_start.strftime('%H:%M'),
                'expertise': reservation.expertiseID.name,
                'status': reservation.get_status_display(),
            }
            for reservation in reservations
        ],
    }
    print('context = ', context)

    return JsonResponse(context)




#reservation id required
#以下為reservation狀態改變

def reservationStCF(request, reservation_id):
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.update_status(1)  # Update the status to "checkin Failed"
        reservation.save()
        return JsonResponse({'status': 'success', 'message': 'Status updated to checkin Failed'})
    except Reservation.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Reservation not found'}, status=404)

def reservationStSc(request, reservation_id):
    if request.method == 'POST':
        try:
            reservation = Reservation.objects.get(pk=reservation_id)
            print(' ', reservation)
            reservation.update_status(2)  # Update the status to "checkin successed"
            reservation.save()
            return JsonResponse({'status': 'success', 'message': 'Status updated to checkin successed'})
        except Reservation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Reservation not found'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def reservationStIt(request, reservation_id):
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.update_status(3)  # Update the status to "in treatment"
        reservation.save()
        return JsonResponse({'status': 'success', 'message': 'Status updated to in treatment'})
    except Reservation.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Reservation not found'}, status=404)

def reservationStFn(request, reservation_id):
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.update_status(4)  # Update the status to "Treatment finished"
        reservation.save()
        # 下次預約
        return JsonResponse({'status': 'success', 'message': 'Status updated to Treatment finished'})
    except Reservation.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Reservation not found'}, status=404)

def reservationStCbD(request, reservation_id):
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.update_status(5)  # Update the status to "cancelled by doc"
        reservation.save()
        return JsonResponse({'status': 'success', 'message': 'Status updated to cancelled by doc'})
    except Reservation.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Reservation not found'}, status=404)

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
	return render(request, 'myApp/doctor_reserve.html', context)


#診所預約按鈕按下去
'''def clinic_reserve_page(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    clinic = {
        'id': clinic.id,
        'name': clinic.name,
        'phone_number': clinic.phone_number,
        'address': clinic.address,
        'introduction':clinic.introduction,
        # 添加其他需要的字段
    }

    return JsonResponse({'clinic': clinic})'''
#先試用render看看
def clinic_reserve_page(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    context = {
        'clinic': clinic
    }
    return render(request, 'myApp/clinic_reserve.html', context)


#各個醫生的專長
def clinic_reserve_doctor_confirmed(request):
    if request.method == 'POST':
        try:
            # 解析 JSON 数据
            data = json.loads(request.body)
            doctor_id = data.get('doctor_id')

            # 保存 doctor_id 到 session
            request.session['doc_id'] = doctor_id

            # 查询医生的专业领域
            doctor_expertise = Doc_Expertise.objects.filter(DocID=doctor_id).select_related('Expertise_ID')

            # 创建专业领域列表
            doc_expertise_list = []

            for expertise in doctor_expertise:
                expertise_dict = {
                    'expertise_name': expertise.Expertise_ID.name,
                    'expertise_time': expertise.Expertise_ID.time
                }
                doc_expertise_list.append(expertise_dict)

            # 存储专业领域列表到 session
            request.session['expertise_list'] = doc_expertise_list

            # 返回 JSON 响应
            return JsonResponse({'expertise_list': doc_expertise_list}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def doctorPage_loading(request):
    user = request.user
    doctor = get_object_or_404(Doctor, id=user.id)
    # working_hours = WorkingHour.objects.filter(DoctorID=doctor)
    
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    schedules = Scheduling.objects.filter(
        DoctorID=doctor,
        StartDate__lte=end_of_week,
        EndDate__gte=start_of_week
    ).select_related('WorkingHour')
    
    reservations = Reservation.objects.filter(
        SchedulingID__in=schedules,
        Status__in=[0, 2, 3],
        time_start__date__range=[start_of_week, end_of_week]
    )

    reservation_list = []
    for reservation in reservations:
        client_name = reservation.ClientID.name
        client_gender = reservation.ClientID.gender
        if client_gender == 'male':
            client_name += " 先生"
        elif client_gender == 'female':
            client_name += " 小姐"
        
        day_of_week = reservation.time_start.strftime('%A')
        reservation_list.append({
            'id': reservation.id,
            'client_name': client_name,
            'appointment_date': reservation.time_start.date().isoformat(),
            'day_of_week': day_of_week,
            'starting': reservation.time_start.time().strftime('%H:%M'),
            'expertise': reservation.expertiseID.name,
            'status': reservation.get_status_display(),
        })
    


    schedule_list = [
        {
            'work_day': schedule.WorkingHour.get_day_of_week_display(),
            'work_start_time': schedule.WorkingHour.start_time.strftime('%H:%M'),
            'work_end_time': schedule.WorkingHour.end_time.strftime('%H:%M'),
            'valid_from': schedule.StartDate,
            'valid_to': schedule.EndDate,
            'WDforfront': schedule.WDforFront(),
            'OccupiedHour': Reservation().TimeSlotNumber(
                start_time=schedule.WorkingHour.start_time,
                end_time=schedule.WorkingHour.end_time
            ),
        }
        for schedule in schedules
    ]

    context = {
        'reservation_list': reservation_list,
        'schedule_list': schedule_list,
    }
    
    return JsonResponse(context)

@login_required        
def clientRecord_loading(request):
    user = request.user
    client = Client.objects.get(id=user.id)
    reservations = Reservation.objects.filter(ClientID=client).order_by('-time_start')
    
    reservation_list = []
    for reservation in reservations:
        scheduling = reservation.SchedulingID
        doctor = scheduling.DoctorID
        clinic = doctor.clinicID
        reservation_list.append({
            'id': reservation.id,
            'appointment_date': reservation.time_start.strftime('%Y-%m-%d'),
            'appointment_time': reservation.time_start.strftime('%H:%M'),
            'expertise': reservation.expertiseID.name,
            'doctor_name': doctor.name,
            'clinic_name': clinic.name,
            'status': reservation.get_status_display(),
        })

    context = {
        'reservation_list': reservation_list,
    }
    print('context = ', context)
    return JsonResponse(context)

#預約頁面日期選下去，計算可預約時間

def add_times(time1, duration):
    # Helper function to add a timedelta to a time object
    datetime1 = datetime.combine(datetime.min, time1)
    result_datetime = datetime1 + duration
    return result_datetime.time()

def available(request):
    # Get doctor_id, date, and expertise_name from the GET request
    doctor_id = request.get('doctor_id')
    date_str = request.GET.get('date')
    date_reserve = datetime.strptime(date_str, '%Y-%m-%d').date()
    week_day = date_reserve.weekday()+1


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
        if schedule.EndDate >= now().date():  # Only include future schedules
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
        if schedule['start_date'] <= date_reserve <= schedule['end_date'] and schedule['day_of_week'] == week_day:
            available = {
                'start_time': schedule['start_time'],
                'end_time': schedule['end_time']
            }
            time_available.append(available)


    # Remove reserved times from available times
    for reservation in reservation_list:
        if reservation['date'] == date_reserve:
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
    expertise_duration = timedelta(hours=expertise_time.hour, minutes=expertise_time.minute, seconds=expertise_time.second)
    for available in consolidated_time_available:
        start = available['start_time']
        while add_times(start, expertise_duration) <= available['end_time']:
            reserve_choices.append(start.strftime('%H:%M:%S'))
            start = add_times(start, expertise_duration)


    # Return available reservation choices as a JSON response
    return JsonResponse({'reserve_choices': reserve_choices})


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


def home(request):
    context={}
    return render(request, "myApp/searchPage.html", context)

def cliedataEd(request):
    context={}
    return render(request, "myApp/client_dataEdit.html", context)

def clinDataEd(request):
    context={}
    return render(request, "myApp/clinic_dataEdit.html", context)

def docDataEd(request):
    context={}
    return render(request, "myApp/doctor_dataEdit.html", context)

def docDataEd(request):
    context={}
    return render(request, "myApp/doctor_dataEdit.html", context)

def clickSchedule(request):
    context={}
    return render(request, "myApp/ClicktoEditSchedule.html", context)

def clickScheduleNew(request):
    context={}
    return render(request, "myApp/ClicktoEditSchedule_New.html", context)

def loginP(request):
    context={}
    return render(request, "myApp/login.html", context)


def clinHome(request):
    context={}
    return render(request, "myApp/clinicPage.html", context)


def docManage(request):
    context={}
    return render(request, "myApp/doctor_management.html", context)


def docPage(request):
    context={}
    return render(request, "myApp/doctorPage.html", context)


def clieReserveRecord(request):
    context={}
    return render(request, "myApp/UserAppointmentRecords.html", context)


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


def check_authentication(request):
    if request.user.is_authenticated:
        return JsonResponse({'is_authenticated': True})
    else:
        return JsonResponse({'is_authenticated': False})
    
def doctor_info(request):
    if hasattr(request.user, 'doctor'):
        user = request.user
        info = {
            'email': user.email,
            'name': user.name,
            'phone_number': user.phone_number,
            'password': user.password,
            #'photo_url': user.doctor.photo.url,
            'experience': user.doctor.experience,
        }
        if user.doctor.photo and user.doctor.photo.name:
           info['photo'] =  user.doctor.photo.url
        return JsonResponse({'status': 'success', 'data': info}, status=200)
    else:
        return JsonResponse({'status': 'error', 'error': 'User is not a doctor'}, status=400)
   
def clinic_info(request):
    if hasattr(request.user, 'clinic'):
        user = request.user
        info = {
            'email': user.email,
            'name': user.name,
            'phone_number': user.phone_number,
            'password': user.password,
            'address': user.clinic.address,
            'license_number': user.clinic.license_number,
            'introduction': user.clinic.introduction,
        }
        if 'photo' in info:
            del info['photo']
        print('photo = ', user.clinic.photo, '  name = ', user.clinic.photo.name)
        print("info = ", info)
        return JsonResponse({'status': 'success', 'data': info}, status=200)
    else:
        return JsonResponse({'status': 'error', 'error': 'User is not a clinic'}, status=400)

def client_info(request):
    if hasattr(request.user, 'client'):
        user = request.user
        info = {
            'email': user.email,
            'name': user.name,
            'phone_number': user.phone_number,
            'password': user.password,
            'address': user.client.address,
            'birth_date': user.client.birth_date,
            'gender': user.client.gender,
            'occupation': user.client.occupation,
            'notify': user.client.notify,
        }
        print("info = ", info)
        return JsonResponse({'status': 'success', 'data': info}, status=200)
    else:
        return JsonResponse({'status': 'error', 'error': 'User is not a client'}, status=400)


#如果是Status = 2或3的話 就不執行而是跳jsonresponse
#變數名有待確認
def client_cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return JsonResponse({'dlteSuccess': True, 'message': 'Reservation cancelled successfully'})


@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        print('logged out')
        return JsonResponse({'message': 'Logged out successfully', 'status': 'success'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


def check_reservations(request):
    now = now()
    #one_hour_ago = now - timedelta(hours=1)


    reservations = Reservation.objects.filter(status=0)


    for reservation in reservations:
        if reservation.time_start < now:
            reservation.status = 1
            reservation.save()


    return JsonResponse({'message': 'Checked and updated reservations if necessary.'})

def get_expertise_list_doc(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    print('getDoc_exp')
    expertise_list = [{'id': de.Expertise_ID.id, 'name': de.Expertise_ID.name, 'time': de.Expertise_ID.time} for de in doctor.doctorID_exp.all()]
    return JsonResponse({'expertise_list': expertise_list})

def get_expertise_list_clin(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    doctors = Doctor.objects.filter(clinicID=clinic_id)
    doctor_expertise = Doc_Expertise.objects.filter(DocID__in=doctors).select_related('Expertise_ID')
    print('getClin_exp')
    expertise_set = set()
    for de in doctor_expertise:
        expertise_set.add((de.Expertise_ID.id, de.Expertise_ID.name))

    expertise_list = [{'id': exp_id, 'name': exp_name} for exp_id, exp_name in expertise_set]
    return JsonResponse({'expertise_list': expertise_list})

def get_doctor_from_exp(request, expertise_id):
    matching_doctors = Doc_Expertise.objects.filter(Expertise_ID=expertise_id).select_related('DocID')

    doctor_list = []

    for de in matching_doctors:
        print('add')
        doctor_list.append({
            'id': de.DocID.id,
            'name': de.DocID.name,
        })
    print(" ", doctor_list)
    return JsonResponse({'doctor_list': doctor_list})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.Status = 5  # Set status to 'cancelled by doc'
    reservation.save()
    return JsonResponse({'status': 'success', 'message': 'Reservation status updated to cancelled.'})