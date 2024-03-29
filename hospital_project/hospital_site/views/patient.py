from django.shortcuts import render, redirect, get_object_or_404

from hospital_site.models import *
from datetime import datetime
from django.core.paginator import Paginator

def home(request):
    return render(request, 'patient/home.html')

def register(request):
    doctors = Doctor.objects.all()
    departments = Department.objects.all()

    # 获取查询值
    name_query = request.GET.get('name', '')
    dept_query = request.GET.get('department', '')
    
    if name_query:
        doctors = doctors.filter(name__contains=name_query)
    
    if dept_query:
        doctors = doctors.filter(dept=dept_query)

    # 分页
    paginator = Paginator(doctors, 10)
    page_number = request.GET.get('page')
    doctors = paginator.get_page(page_number)

    # 转换为int在前端进行比较
    dept_query = int(dept_query, base=10) if dept_query != '' else dept_query
    
    return render(request, 'patient/register.html', {'doctors': doctors, 'name_query': name_query, 'dept_query': (dept_query), 'departments' : departments})
    
def register_sucess(request):
    return render(request, 'patient/register_success.html')

def register_appoint(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)

    if request.method == 'POST':
        appointment_time = request.POST.get('appointment_time')
        period = request.POST.get('period')

        # 将字符串时间转换为datetime对象
        appointment_datetime = datetime.strptime(appointment_time, '%Y-%m-%d')

        # 通过session获得患者实例
        patient = Patient.objects.get(id=request.session.get('info')['id'])

        # 创建挂号记录
        registration = Registration.objects.create(
            doctor=doctor,
            patient=patient,
            registration_time=appointment_datetime,
            period=period,
            status=0,
        )

        return redirect('/patient/register/success/')

    options = Registration.PERIOD_CHOICES
    return render(request, 'patient/register_appoint.html', {'doctor': doctor, 'options': options})

def registrations(request):
    patient_id = request.session.get('info')['id']
    patient = Patient.objects.get(id=patient_id)
    registrations = Registration.objects.filter(patient=patient)

    # 分页
    paginator = Paginator(registrations, 10)
    page_number = request.GET.get('page')
    registrations = paginator.get_page(page_number)

    return render(request, 'patient/registrations.html', {'registrations':registrations})

def cancel_registration(request, registration_id):
    registration = get_object_or_404(Registration, pk=registration_id)
    if registration.status == 0:
        registration.status = 1
        registration.save()
    
    return redirect('/patient/registrations/')


def personnel(request):
    doctors = Doctor.objects.all()
    departments = Department.objects.all()
    return render(request, 'patient/personnel.html', {'doctors': doctors, 'departments': departments})

def profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    return render(request, 'patient/profile.html', {'doctor': doctor})

def medical_record(request, registration_id):
    registration = get_object_or_404(Registration, pk=registration_id)
    medical_record = MedicalRecord.objects.get(registration=registration)
    return render(request, 'patient/medical_record.html', {'medical_record': medical_record})

def personal(request):
    patient_id = request.session.get('info')['id']
    patient = Patient.objects.get(id=patient_id)
    return render(request, 'patient/personal.html', {'patient': patient})