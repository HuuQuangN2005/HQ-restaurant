from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import AccountViewSet, PhoneViewSet, AddressViewSet

router = DefaultRouter()
router.register(r"accounts/me/phones", PhoneViewSet, basename="user-phones")
router.register(r"accounts/me/addresses", AddressViewSet, basename="user-addresses")
router.register(r"accounts", AccountViewSet, basename="account")

urlpatterns = [
    path("", include(router.urls)),
]
