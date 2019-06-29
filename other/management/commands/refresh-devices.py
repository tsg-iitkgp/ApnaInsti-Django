"""Refresh all devices with info from FCM."""
from django.conf import settings
from django.core.management.base import BaseCommand
from pyfcm import FCMNotification

from helpers.device import fill_device_firebase
from other.models import Device


class Command(BaseCommand):
    help = 'Sends push notifications of event starting'

    def handle(self, *args, **options):
        # Initiate connection
        push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)

        # Refresh all
        for device in Device.objects.all():
            print(device.user.name + ' - ', end='', flush=True)
            if fill_device_firebase(push_service, device):
                print('OK')
            else:
                device.delete()
                print('FAIL')
