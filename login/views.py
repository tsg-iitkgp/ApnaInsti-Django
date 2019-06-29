"""Login Viewset."""
import requests
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response

from login.helpers import perform_login, perform_signup, valid_insti_id
from users.models import UserProfile
from users.serializer_full import UserProfileFullSerializer

# pylint: disable=C0301

class LoginViewSet(viewsets.ViewSet):
    """Login"""

    @staticmethod
    def signup(request):
        """
        Signup using institute email ID.

        Signup using a user's institute email ID and send them a password over there.
        """

        # Check if we have the institute email ID
        instiID = request.GET.get('username')
        if instiID is None:
            return Response({"message": "instituteID is required"}, status=400)

        if not valid_insti_id(instiID):
            return Response({"message": "instituteID is not valid"}, status=400)

        return perform_signup(instiID, request)

    @staticmethod
    def pass_login(request):
        """
        Login using institute email address and password.
        """

        # Check if we have the username
        username = request.GET.get('username')
        if username is None:
            return Response({"message": "{?username} is required"}, status=400)

        # Check if we have the password
        password = request.GET.get('password')
        if password is None:
            return Response({"message": "{?password} is required"}, status=400)

        if User.objects.filter(username=username).first() is None:
            return Response({"message": "no user with {} found".format(username)}, status=404)

        return perform_login(request)

    @staticmethod
    def get_user(request):
        """Get session and profile."""

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({"message": "not logged in"}, status=401)

        # Check if the user has a profile
        try:
            queryset = UserProfileFullSerializer.setup_eager_loading(UserProfile.objects)
            user_profile = queryset.get(user=request.user)
            profile_serialized = UserProfileFullSerializer(
                user_profile, context={'request': request})
        except UserProfile.DoesNotExist:
            return Response({'message': "UserProfile doesn't exist"}, status=500)

        # Return the details and nested profile
        return Response({
            'sessionid': request.session.session_key,
            'user': request.user.username,
            'profile_id': user_profile.id,
            'profile': profile_serialized.data
        })

    @staticmethod
    def logout(request):
        """Log out."""

        logout(request)
        return Response({'message': 'logged out'})
