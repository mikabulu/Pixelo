from .models import User
from rest_framework import serializers


class UserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email',)