from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
# router.register('users', UserView)
router.register('departments', DepartmentView)
router.register('designations', DesignationView)
router.register('employees', EmployeeView)
router.register('attendances', AttendanceView)

urlpatterns = router.urls