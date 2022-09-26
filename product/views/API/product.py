import json
import re
from urllib import request
from django.conf import settings
from django.db.models import Q 

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
import requests
import json

from product.serializers import ProductSerializer
from product.models import Product
from product.permission import *
from product.permission import CustomePermission
from weather.models import Weather
from weather.views.API.weather import get_current_temp

class ProductListCreateAPIView(ListCreateAPIView):
    
    serializer_class = ProductSerializer
    queryset = Product.objects.filter()
    permission_classes = [CustomePermission,]

    def get_permissions(self):
        if self.request.method == "GET":
            return (permissions.AllowAny(),)
        return super().get_permissions()

    def create(self, request, *args, **kwargs):

        ##storing owner in product model
        get_owner = request.user.id
        request.data['owner'] = get_owner

        ##storing weather type in product model
        get_weather_id = request.data['weather_tag']
        get_weather_name = list(Weather.objects.filter(id__in=get_weather_id).values_list('name', flat=True))
        request.data['weather_tag'] = get_weather_name

        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'201', 'msg': 'created successfully', 'data':serializer.data, }, status.HTTP_201_CREATED,)
        return Response({'status':'400', 'msg': 'Please Insert Correct value', 'data':serializer.errors, }, status.HTTP_400_BAD_REQUEST,)  
       
    def list(self, request):

        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        return Response({ "response": status.HTTP_200_OK,"message":"showing data","data":serializer.data}) 



class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [CustomePermission,]
    lookup_field = 'pk'


    def get_permissions(self):
        if self.request.method == "GET":
            return (permissions.AllowAny(),)
        return super().get_permissions()


    def get(self, request, pk, *args, **kwargs):
        try:
            product              = Product.objects.get(id=pk)
            serializer           = ProductSerializer(product)
        except Exception as e:
            return Response({'status':'404', 'msg': str(e) }, status.HTTP_404_NOT_FOUND,)  

        return Response({'status':'200', 'msg': 'showing data', 'data':serializer.data, }, status.HTTP_200_OK,)
   
    def put(self,request,pk,format=None):

        try:
            product        = Product.objects.get(id=pk)
            serializer  = ProductSerializer(product, data=request.data, partial = True)

        except Exception as e:
            return Response({'status':'404', 'msg': str(e) }, status.HTTP_404_NOT_FOUND,)  

        if serializer.is_valid():
            serializer.save()
            return Response({'status':'200', 'msg': 'data updated', 'data':serializer.data, }, status.HTTP_200_OK,)
        return Response({'status':'400', 'msg': 'Please Insert Correct value', 'data':serializer.errors, }, status.HTTP_400_BAD_REQUEST,)  


    def delete(self,request,pk,format=None):
        try:
            product        = Product.objects.get(id=pk)
        except Exception as e:
            return Response({'status':'404', 'msg': str(e) }, status.HTTP_404_NOT_FOUND,)  

        product.delete()
        return Response({'status':'200', 'msg': 'data deleted', }, status.HTTP_200_OK,)

  

class SearchResultsView(ListCreateAPIView):

    def get_permissions(self):

        if self.request.method == 'GET':
            return (permissions.AllowAny(),)

    def list(self, request, *args, **kwargs):

        query = self.request.GET.get("q")
        
        product              = Product.objects.filter(Q(name__icontains = query) | Q(weather_tag__icontains = query))
        if not product:
            return Response({'status':'404', 'msg': 'no data found' }, status.HTTP_404_NOT_FOUND,)  

        serializer           = ProductSerializer(product, many = True)
        return Response({'status':'200', 'msg': 'showing data', 'data':serializer.data, }, status.HTTP_200_OK,)



class ProductRecommendationView(ListCreateAPIView):

    def get_permissions(self):

        if self.request.method == 'GET':
            return (permissions.AllowAny(),)

    def list(self, request, *args, **kwargs):

        get_current_weather = get_current_temp(request)
        if get_current_weather:
            # get_weather_name = Weather.objects.get(name=get_current_weather)
            # print(get_current_weather)
            product              = Product.objects.filter(weather_tag__icontains=get_current_weather)
            if not product:
                return Response({'status':'404', 'msg': 'no data found' }, status.HTTP_404_NOT_FOUND,)  
            serializer           = ProductSerializer(product, many = True)
            return Response({'status':'200', 'msg': 'showing data', 'data':serializer.data, }, status.HTTP_200_OK,)
        else:
            return Response({'status':'404', 'msg': 'no data found' }, status.HTTP_404_NOT_FOUND,)  
