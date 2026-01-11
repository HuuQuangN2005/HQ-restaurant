from rest_framework import viewsets, permissions, mixins
from actions.permissions import IsCommentOwner
from actions.serializers import (
    CommentSerializer,
    ReservationSerializer,
    SimpleOrderSerializer,
    OrderSerializer,
)
from actions.models import Comment, Reservation, Order
from restaurant.permissions import IsStaff


class CommentViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwner]
    lookup_field = "uuid"

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.filter(is_active=True)
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "uuid"
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(account=self.request.user)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(is_active=True)
    lookup_field = "uuid"
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        if self.action in ["partial_update", "destroy"]:
            return [IsStaff()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset

        queryset = queryset.select_related("account", "address").prefetch_related(
            "details__food"
        )

        if user.is_staff:
            return queryset
        return queryset.filter(account=user)

    def get_serializer_class(self):
        if self.action == "list":
            return SimpleOrderSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
