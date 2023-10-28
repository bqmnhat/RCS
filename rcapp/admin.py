from django.contrib import admin
from rcapp.models import Patient, Doctor, Specialist, TimeTable


# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Specialist)
admin.site.register(TimeTable)