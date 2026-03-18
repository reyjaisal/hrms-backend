from .models import *
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

# Helper function to set attendance for current day
# employees should be objects of Employee model
def set_current_day_attendance(employees):
    # create attendance object for current day with absent status for all employees if not exist
    existing_attendances_ids = list(Attendance.objects.filter(day=datetime.now().date(), employee__in=employees).values_list("employee_id", flat=True))
    if existing_attendances_ids:
        employees = employees.exclude(id__in=existing_attendances_ids)
        
    for employee in employees:
        _ , created = Attendance.objects.get_or_create(employee=employee, day=datetime.now().date(), defaults={"status": "Absent"})
        if created:
            logger.info(f"[INFO] Attendance created for employee {employee.full_name} with status Absent")