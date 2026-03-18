# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
# from rest_framework import status
from .models import *
from .serializers import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from .helpers import set_current_day_attendance

# Logger
import logging
logger = logging.getLogger(__name__)

class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def create_user(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            serialized = self.get_serializer(user, many=True)

            return Response({
                "success": True,
                "user": serialized.data
            }, status=status.HTTP_201_CREATED)


class DepartmentView(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DesignationView(ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer


class EmployeeView(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # Get employees method
    @action(detail=False, methods=['get'])
    def get_employees(self, request):
        context = {"success": False}
        try:
            employee_name_filter = request.GET.get("employee_name", None)
            employees = self.get_queryset().all()
            total_count = employees.filter(archived=False).count()
            total_resigned_count = employees.filter(archived=True).count()

            # Apply employee name filter if exist
            employees = employees.filter(full_name__icontains=employee_name_filter) if employee_name_filter else employees
            all_employees_serializer = self.get_serializer(employees.filter(archived=False), many=True)
            resigned_employees_serializer = self.get_serializer(employees.filter(archived=True), many=True)

            departments = list(Department.objects.filter(archived=False).values("id", "name"))
            designations = list(Designation.objects.filter(archived=False).values("id", "name"))

            context = {
                "success": True,
                "all_employees": all_employees_serializer.data,
                "resigned_employees": resigned_employees_serializer.data,
                "total_count": total_count,
                "resigned_count": total_resigned_count,
                "tab_total_count": employees.filter(archived=False).count(),
                "tab_resigned_count": employees.filter(archived=True).count(),
                "departments": departments,
                "designations": designations,
                "new_count": 0
            }
        except Exception as e:
            logger.error(f"[ERROR] {str(e)}")

        return Response(context, status=status.HTTP_200_OK)
    
    # Get employees details
    @action(detail=True, methods=['get'])
    def get_employee(self, request, pk=None):
        context = {"success": False}
        try:
            employee = self.get_queryset().filter(archived=False).get(pk=pk)
            serializer = self.get_serializer(employee)

            context = {
                "success": True,
                "data": serializer.data
            }
        except Exception as e:
            logger.error(f"[ERROR] {str(e)}")

        return Response(context, status=status.HTTP_200_OK if context["success"] else status.HTTP_404_NOT_FOUND)
    

    # Update employees details
    @action(detail=True, methods=['put'])
    def update_employee(self, request, pk=None):
        context = {"success": False}
        try:
            data = request.data
            employee = self.get_queryset().filter(archived=False).get(pk=pk)

            # Update fields
            first_name = data.get("first_name", employee.user.first_name)
            last_name = data.get("last_name", employee.user.last_name)
            full_name = f"{first_name} {last_name}"
            employee.full_name = full_name
            employee.experience = data.get("experience", employee.experience)

            # Update relation data
            department_id = data.get("department")
            designation_id = data.get("designation")

            if department_id:
                employee.department = Department.objects.filter(id=department_id).first()
            if designation_id:
                employee.designation = Designation.objects.filter(id=designation_id).first()

            # update skills
            skills =  request.POST.getlist("skills", [])
            if skills:
                employee.skills = ", ".join(skills)

            employee.save()
            serializer = self.get_serializer(employee)

            context = {
                "success": True,
                "data": serializer.data
            }

        except Exception as e:
            logger.error(f"[ERROR] {str(e)}")

        return Response(context, status=status.HTTP_200_OK if context["success"] else status.HTTP_404_NOT_FOUND)


    # Add Employee
    @action(detail=False, methods=['post'])
    def add_employee(self, request):
        context = {"success": False}

        if request.method == "POST":
            try:
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                email = request.POST.get("email")
                password = request.POST.get("password")
                department_id = request.POST.get("department")
                designation_id = request.POST.get("designation")
                skills = request.POST.getlist("skills", [])
                experience = request.POST.get("experience") or "0"
                activate_existing_user = request.POST.get("restore_archived_employee", False) == "true"
                username = f"hrms_{first_name.lower()}"

                # Initial user data
                user_data = {
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": password,
                }

                # Check if user exist with same email
                user = User.objects.filter(email=email).first()


                # Creating User First or restoring existing
                if not user or (user and activate_existing_user):
                    if not user:
                        user_serializer = UserSerializer(data=user_data)
                        if user_serializer.is_valid():
                            user = user_serializer.save()
                        else:
                            logger.error("[ERROR] Validation issue while creating User")
                    
                    # Create Employee
                    if user:
                        employe_data = {
                            "full_name": f"{first_name} {last_name}",
                            "employee_id": f"DEV{user.id}",
                            "email": email,
                            "department": department_id,
                            "designation": designation_id,
                            "skills": ", ".join(skills) if skills else "",
                            "experience": experience
                        }
                    
                        employees = Employee.objects.filter(user=user)
                        # Restore Employee if already exist
                        if employees.exists():
                            employees.update(archived=False)
                            context["success"] = True
                        else:
                            # Save new Employee
                            employee_serilizer = EmployeeSerializer(data=employe_data)
                            if employee_serilizer.is_valid():
                                employee_serilizer.save(user=user)
                                context["success"] = True
                            elif user:
                                logger.info("[INFO] User is created but validation issue while creating employee")
                else:
                    if user and not activate_existing_user:
                        exist_emp = self.get_queryset().filter(user=user)
                        context['user_exist'] = exist_emp.filter(archived=False).exists()
                        context['need_activation_confirmation'] = exist_emp.filter(archived=True).exists()
                        context['info'] = "User with this email already exist, if you want to activate this user then please check the activate existing user option"
            except Exception as e:
                logger.error(f"[ERROR] {str(e)}")
                context['error'] = "Something went wrong, please refresh and try again later!"
        else:
            logger.error("[ERROR] Incorrect method used for creating new employee")

        return Response(context, status=status.HTTP_200_OK)
    

    # Get employees details
    @action(detail=True, methods=['delete'])
    def archive_employee(self, request, pk=None):
        context = {"success": False}
        try:
            employee = self.get_queryset().filter(archived=False).get(pk=pk)
            employee.archived = True
            employee.save()
            serializer = self.get_serializer(employee)

            context = {
                "success": True,
                "data": serializer.data
            }
        except Exception as e:
            logger.error(f"[ERROR] {str(e)}")

        return Response(context, status=status.HTTP_200_OK if context["success"] else status.HTTP_404_NOT_FOUND)
    

    @action(detail=True, methods=['patch'])
    def restore_employee(self, request, pk=None):
        context = {"success": False}
        try:
            employee = self.get_queryset().filter(archived=True).get(pk=pk)
            employee.archived = False
            employee.save()
            serializer = self.get_serializer(employee)

            context = {
                "success": True,
                "data": serializer.data
            }
        except Exception as e:
            logger.error(f"[ERROR] {str(e)}")

        return Response(context, status=status.HTTP_200_OK if context["success"] else status.HTTP_404_NOT_FOUND)


class AttendanceView(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(detail=False, methods=['get'])
    def get_calendar_attendance(self, request):
        context = {"success": False}

        try:
            # Get date range from request
            start_date_str = request.GET.get("startDate")
            end_date_str = request.GET.get("endDate")

            if start_date_str and end_date_str:
                start_date = parse(start_date_str)
                end_date = parse(end_date_str)
            else:
                # fallback (optional)
                today = datetime.today()
                start_date = datetime(today.year, today.month, 1)
                end_date = start_date + relativedelta(months=1)

            # Get all employees
            employees = Employee.objects.filter(archived=False)

            # Update current day attendance for all employees if not set already
            set_current_day_attendance(employees)

            # get current month attendances
            attendances = self.get_queryset().filter(archived=False, day__range=(start_date, end_date))

            attendance_data = []
            for day in range(1, 32):  # Loop through possible days in a month
                day_attendances = attendances.filter(day__day=day)
                if day_attendances.exists():
                    attendance_summary = day_attendances.values('status').annotate(count=models.Count('id'))
                    attendance_counts = {item['status']: item['count'] for item in attendance_summary}
                    attendance_data.append({
                        "date": day_attendances.first().day.strftime("%Y-%m-%d"),
                        "attendance_data": attendance_counts
                    })

            context = {
                "success": True,
                "data": attendance_data,
                "current_date": datetime.now().strftime("%Y-%m-%d")
            }
        except Exception as e:
            logger.error(f"[ERROR] {str(e)}")

        return Response(context, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'])
    def get_listview_attendance(self, request):
        context = {"success": False}

        try:
            attendance_date = request.GET.get("attendance_date")

            if attendance_date:
                day = parse(attendance_date)
            else:
                # fallback (optional)
                day = datetime.today()

            is_current_day = day.date() == datetime.now().date()

            # Get all employees
            employees = Employee.objects.filter(archived=False)

            # Update current day attendance for all employees if not set already
            set_current_day_attendance(employees)

            # get current month attendances
            attendances_query = self.get_queryset().filter(archived=False, day=day)
            attendance = self.get_serializer(attendances_query, many=True)
            
            context = {
                "success": True,
                "data": attendance.data,
                "current_date": day.strftime("%Y-%m-%d"),
                "is_current_day": is_current_day
            }
        except Exception as e:
            logger.error(f"[ERROR] {str(e)}")

        return Response(context, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=['patch'])
    def mark_attendance(self, request, pk):
        context = {"success": False}

        try:
            new_status = request.POST.get("status")

            current_date = datetime.now().date()

            # Get all employees
            attendance = self.get_queryset().filter(archived=False, day=current_date, employee__id=pk).first()
            attendance.status = new_status
            attendance.save()

            serializer = self.get_serializer(attendance)

            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_202_ACCEPTED)
            
        except Exception as e:
            logger.error(f"[ERROR] {str(e)}")

        return Response(context, status=status.HTTP_200_OK)