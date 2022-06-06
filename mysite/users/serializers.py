
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User,Message
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from uuid import uuid4


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(max_length=8)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'ifLogged'
        )

class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username 
    username = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,password validator
        username = data.get("username", None)
        password = data.get("password", None)
        if not username and not password:
            raise ValidationError("Details not entered.")
        user = User.objects.get(username=username)    
        if not check_password(password,user.password):
                raise ValidationError("User credentials are not correct.")      
        if user.ifLogged:
            raise ValidationError("User already logged in.")  
        user.ifLogged = True   
        data['token'] = uuid4() 
        user.token = data['token']  
        user.save()    
        return data

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'token',
        )

        read_only_fields = (
            'token',
        )

class UserLogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        username = data.get("username",None)
        try:
            user = User.objects.get(username = username)
            if not user.ifLogged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.ifLogged = False
        user.token = ""
        user.save()
        data['status'] = "User is logged out."
        return data

    class Meta:
        model = User
        fields = (
            'token',
            'status',
            'username',
        )


class MessageSerializer(serializers.ModelSerializer):



    class Meta:
        model = Message
        fields = (
            'pk'
            'receiver',
            'created',
            'subject',
            'text',
            'isRead',
        )


class ReadMessageSerializer(serializers.ModelSerializer):

    def validate(self,data):
        receiver = data.get("receiver",None)
        try:
            user = User.objects.get(username = receiver)
            if not user.ifLogged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        return data

    class Meta:
        model = Message
        fields = (
            'pk',
            'receiver',
            'isRead',
        )