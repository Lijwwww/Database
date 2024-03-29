from django.contrib import admin
from hospital_site import models


class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "username", "password", "gender")

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "room_number")

class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "username", "password", "title", "dept_id", "profile")

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("id", "doctor_id", "patient_id", "registration_time", "period", "status")

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "symptom", "diagnosis", "solution", "registration_id")

class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "producer", "price")

admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.Registration, RegistrationAdmin)
admin.site.register(models.MedicalRecord, MedicalRecordAdmin)
admin.site.register(models.Medicine, MedicineAdmin)