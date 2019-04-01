"""Circle views."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cride.circles.models import Circle
from cride.circles.serializers.circles import CircleModelSerializer


class CircleViewSet(viewsets.ModelViewSet):
    """Circle view set."""

    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Circle.objects.all()
        if self.action == 'list':
            queryset = queryset.filter(is_public=True)
        return queryset
