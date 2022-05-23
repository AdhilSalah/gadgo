
from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    

    class Meta:
        model = CustomUser
        fields = ['email','password','is_email_verified']
