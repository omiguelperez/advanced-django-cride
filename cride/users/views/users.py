"""User views."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cride.users.serializers.users import UserLoginSerializer, UserModelSerializer


class UserLoginAPIView(APIView):
    """User login API view."""

    def post(self, request):
        """Handle HTTP POST request."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token.key
        }
        return Response(data, status=status.HTTP_201_CREATED)
