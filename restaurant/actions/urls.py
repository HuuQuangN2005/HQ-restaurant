from django.urls import path, include
from rest_framework.routers import DefaultRouter
from actions.views import CommentViewSet, ReservationViewSet, OrderViewSet


router = DefaultRouter()

router.register("comments", CommentViewSet, basename="comment")
router.register("reservations", ReservationViewSet, basename="reservation")
router.register("orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
