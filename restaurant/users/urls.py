from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import EmployeeViewSet, CustomerViewSet

router = DefaultRouter()


router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"customers", CustomerViewSet, basename="customer")

urlpatterns = [
    path("users/", include(router.urls)),
]
