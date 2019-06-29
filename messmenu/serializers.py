"""Serializers for mess menu."""
from rest_framework import serializers

from messmenu.models import Hostel, MenuEntry


class MenuEntrySerializer(serializers.ModelSerializer):
    """Serializer for one mess menu entry."""
    class Meta:
        model = MenuEntry
        fields = '__all__'

class HostelSerializer(serializers.ModelSerializer):
    """Serializer for the hostel model"""
    mess = MenuEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Hostel
        fields = ('id', 'name', 'short_name', 'long_name', 'mess')

    @staticmethod
    def setup_eager_loading(queryset):
        """Perform necessary eager loading of data."""
        queryset = queryset.prefetch_related('mess')
        return queryset
