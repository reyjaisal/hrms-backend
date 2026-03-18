from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    # Create employee using primary key
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    designation = serializers.PrimaryKeyRelatedField(queryset=Designation.objects.all())

    # Read only nested representation of department and designation
    department_details = DepartmentSerializer(source='department', read_only=True)
    designation_details = DesignationSerializer(source='designation', read_only=True)

    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Employee
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
     # Create attendance using primary key
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    # Read only nested representation of employee
    employee_details = EmployeeSerializer(source='employee', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'
