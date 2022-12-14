from django.conf import settings
import requests

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework import permissions, status
from rest_framework.response import Response


from account.serializers import UserSerializer
from account.models import CustomUser


class CustomerListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.filter()

    def get_permissions(self):
      
        if self.request.method == 'GET':
            return (permissions.IsAdminUser(),)
    
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)
        

    def create(self, request, *args, **kwargs):

        try:
            user = CustomUser.objects.create(
                first_name=self.request.data['first_name'],
                last_name=self.request.data['last_name'],
                email=self.request.data['email'],
                username=self.request.data['username'], 
            )   
            try:
                user.user_type = self.request.data['user_type']
            except:
                user.user_type = 'customer'            
            user.set_password(self.request.data['password'])
            user.save()
            serializer = self.get_serializer(user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(data={'message': f'cannot create user. reason: {e}'}, status=status.HTTP_409_CONFLICT)


class UserRoleAPIView(ListCreateAPIView):
    
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'PUT':
            return (permissions.IsAdminUser(),)

    def put(self, request, *args, **kwargs):

        try:
            get_user = request.data['user']
            get_role = request.data['role']

            get_user = CustomUser.objects.get(id=request.data['user'])
            get_user.user_type = request.data['role']
            get_user.save()
            return Response({'status':'200', 'msg': 'data updated', }, status.HTTP_200_OK,)
        except Exception as e:
            print(e)
            return Response(data={'message': f'cannot create user. reason: {e}'}, status=status.HTTP_409_CONFLICT)
