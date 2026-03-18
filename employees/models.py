from django.db import models
from django.contrib.auth.models import User
from datetime import date

status_choice = (
    ("Present","Present"),
    ("Absent","Absent"),
    ("On leave","On leave"),
)

# Department Table
class Department(models.Model):
    name = models.CharField(max_length=255)
    initials = models.CharField(max_length=50, null=True)
    archived = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # check if first time save

        # Save first 4 latters as initials only when creating new department, if name length is less than 4 then save full name as initials
        if is_new:
            self.initials = self.name[:3].upper() if len(self.name) >= 3 else self.name.upper()
        
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

# Designation Table
class Designation(models.Model):
    name = models.CharField(max_length=255)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

# Employee Table
class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    experience = models.CharField(max_length=100, default="0 Years")
    date_of_joining = models.DateField(default=date.today)
    skills = models.CharField(max_length=255, blank=True)  # Comma separated skills
    archived = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        is_new = self.pk is None  # check if first time save
        if not is_new:
            # If employee is being archived, then archive all attendance records of that employee
            Attendance.objects.filter(employee=self).update(archived=self.archived)
            
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name
    

# Attendance Table
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    day = models.DateField(default=date.today)
    status = models.CharField(max_length=255, choices=status_choice)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.employee.full_name + " - " + self.status