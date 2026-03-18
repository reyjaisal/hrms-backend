from django.contrib import admin
from .models import Department, Designation, Employee, Attendance
# Register your models here.

admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Employee)
admin.site.register(Attendance) 
