"""Circle views."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cride.circles.models import Circle
from cride.circles.serializers.circles import CircleModelSerializer


class CircleViewSet(viewsets.ModelViewSet):
    """Circle view set."""

    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)
