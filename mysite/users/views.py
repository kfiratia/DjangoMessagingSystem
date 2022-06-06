from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.shortcuts import get_object_or_404
from .models import User, Message
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer, MessageSerializer, \
    ReadMessageSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response


class RegisterAndShowUsers(generics.ListCreateAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self , serializer):
        password = make_password((self.request.data.get("password")))
        user = User.objects.create(username=self.request.data.get("username"),password = password)
        user.save()


class Login(generics.GenericAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        request.data["token"] = request.headers['x-access-token']
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response("logout success", status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

class AllMessagesForUser(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


    def retrieve(self, request, *args, **kwargs):
        """ userid = self.request.query_params.get('user_id', None) """
        data = list()
        try:
            user = User.objects.get(username = self.kwargs['user'])
            print(user)
        except:
            return Response("User is not register.", status=HTTP_400_BAD_REQUEST)
        if not user.ifLogged:
            return Response("User is not logged in.", status=HTTP_400_BAD_REQUEST)
        queryset = Message.objects.filter(receiver=user)
        print(queryset)
        for message in queryset:
            data.append({"id":message.pk,
                         "sender":message.sender,
                             "receiver":message.receiver,
                             "subject":message.subject,
                            "text":message.text,
                             "created":message.created,
                             "isRead":message.isRead})
        return Response(data)

class AllUnreadMessagesForUser(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


    def retrieve(self, request, *args, **kwargs):
        """ userid = self.request.query_params.get('user_id', None) """
        data = list()
        try:
            user = User.objects.get(username = self.kwargs['user'])
            print(user)
        except:
            return Response("User is not register.", status=HTTP_400_BAD_REQUEST)
        if not user.ifLogged:
            return Response("User is not logged in.", status=HTTP_400_BAD_REQUEST)
        queryset = Message.objects.filter(receiver=user,isRead = False)
        print(queryset)
        for message in queryset:
            data.append({"id":message.pk,
                            "sender":message.sender,
                             "receiver":message.receiver,
                             "subject":message.subject,
                            "text":message.text,
                             "created":message.created,
                             "isRead":message.isRead})
        return Response(data)




class CreateNewMessage(generics.CreateAPIView):
    # get method handler
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self , serializer):
        try:
            sender = User.objects.get(username=self.kwargs['user'])
            print("100!!")
            if sender.ifLogged:
                sender = self.kwargs['user']
            else:
                raise ValidationError('User is not logged in.')
        except:
            raise ValidationError("User is not logged in.")
        try:
            User.objects.get(username=self.request.data.get("receiver"))
            receiver = self.request.data.get("receiver")
        except:
            raise ValidationError('Receiver does not exist')
        subject = self.request.data.get("subject")
        text = self.request.data.get("text")
        message = Message.objects.create(sender=sender,receiver = receiver,subject = subject,text = text)
        message.save()


class ReadMessage(generics.GenericAPIView):
    # get method handler
    queryset = Message.objects.all()
    serializer_class = ReadMessageSerializer

    def put(self, request,pk,user):
        data = [{"receiver":user}]
        try:
            message = Message.objects.get(pk = pk,receiver = user)
        except:
            return Response("The message does not exist", status=HTTP_400_BAD_REQUEST)
        serializer_class = ReadMessageSerializer(message,data=data[0])
        if serializer_class.is_valid(raise_exception=True):
            message.isRead = True
            message.save()
            data.append({"id": message.pk,
                     "sender": message.sender,
                     "subject": message.subject,
                     "text": message.text,
                     "created": message.created,
                     "isRead": message.isRead})
            return Response(data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request,pk,user):
        data = [{"receiver":user}]
        message = Message.objects.get(pk = pk)
        serializer_class = ReadMessageSerializer(message,data=data[0])
        if serializer_class.is_valid(raise_exception=True):
            message.delete()
            return Response("The message has been deleted", status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)