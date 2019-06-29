"""Helpers for login functions."""
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.response import Response

from helpers.device import update_fcm_device
from users.models import UserProfile
from users.serializer_full import UserProfileFullSerializer


# pylint: disable=R0914
def perform_signup(insti_id, request):
    """Perform login with code and redir."""

    # generate random password for the user
    rand_pass = User.objects.make_random_password(length=8)
    user = User.objects.filter(username=insti_id).first()

    # Return if the user already exists
    if user:
        return Response({
            'msg': "user with {username} already exists!".format(username=insti_id)
        })
        
    user = User.objects.create_user(username=insti_id, password=rand_pass) 

    # Check if User has a profile and create if not
    user_profile = UserProfile.objects.create(user=user, name='')

    # # Log in the user
    # login(request, user)
    # request.session.save()

    # Deprecated: update fcm id
    fcm_id = request.GET.get('fcm_id')
    if fcm_id is not None:
        update_fcm_device(request, fcm_id)

    # TODO: Add method to send email to user
    print(rand_pass)
    print(user)

    return Response({
        'msg': "{username} created, please check mail inbox for login details.".format(username=user.username)
    })
    
def perform_login(request):
    """
    Perform login and retain session.
    """
    username = request.GET.get('username')
    password = request.GET.get('password')

    user = authenticate(username=username, password=password)

    if user:
        # load user profile
        queryset = UserProfileFullSerializer.setup_eager_loading(UserProfile.objects)
        user_profile = queryset.get(user=user)
        
        login(request, user)
        # Return the session id
        return Response({
        'sessionid': request.session.session_key,
        'user': user.username,
        'profile_id': user_profile.id,
        'profile': UserProfileFullSerializer(
            user_profile, context={'request': request}).data
    })

    return HttpResponse("Invalid login credentials given!")

def valid_insti_id(insti_mail):
    """
    Validate institute ID that it is valid email address ending with iitkgp.ac.in
    """
    try:
        validate_email(insti_mail)
    except ValidationError as err:
        return False
    
    suffix = insti_mail.split('@')[1]
    if suffix != settings.INSTI_MAIL_SUFFIX:
        return False

    return True
