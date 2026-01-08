from rest_framework import viewsets, permissions, generics


from actions.permissions import IsCommentOwner
from actions.serializers import CommentSerializer
from actions.models import Comment


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView):
    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwner]
    lookup_field = "uuid"
