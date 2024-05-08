from django.shortcuts import render
from django.http import HttpResponse
from .forms import DoctorForm
from .forms import ClinicForm
from .forms import ClientForm

def home(request):
    context={}
    return render(request, "myApp/home.html", context)

def index(request):
    context={}
    return render(request, "myApp/index.html", context)


def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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







