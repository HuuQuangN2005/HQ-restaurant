from rest_framework import viewsets, permissions, generics, mixins


from actions.permissions import IsCommentOwner
from actions.serializers import CommentSerializer, ReservationSerializer
from actions.models import Comment, Reservation


class CommentViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwner]
    lookup_field = "uuid"

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "uuid"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(account=self.request.user)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)