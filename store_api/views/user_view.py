from http.client import HTTPResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from store_api.serializers.user_serializer import UserSerializer
from store_api.models import User
from django.http import JsonResponse
import requests
from rest_framework.views import APIView
from decouple import config


class UserAPI(APIView):
    def get(self, request, format=None):
        print(request.META["HTTP_AUTHORIZATION"])
        url = config('TOKEN_VERIFY')
        params = {"token":request.META["HTTP_AUTHORIZATION"]}
        data = requests.post(url, data=params)
        if data.status_code == 200:
            try:
                user = User.objects.get(token=request.META["HTTP_AUTHORIZATION"])
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist as e:
                return Response({"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED) 
        else:
            return Response({"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        url = config('TOKEN_VERIFY')
        params = {"token":request.META["HTTP_AUTHORIZATION"]}
        data = requests.post(url, data=params)
        if data.status_code == 200:
            try:
                user = User.objects.get(token=request.META["HTTP_AUTHORIZATION"])
                serializer = UserSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'Complete Data Updated'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist as e:
                return Response({"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
       
        

    def patch(self, request, format=None):
        url = config('TOKEN_VERIFY')
        params = {"token":request.META["HTTP_AUTHORIZATION"]}
        data = requests.post(url, data=params)
        if data.status_code == 200:
            try:
                user = User.objects.get(token=request.META["HTTP_AUTHORIZATION"])
                serializer = UserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'Partial Data Updated'}, status=status.HTTP_206_PARTIAL_CONTENT)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist as e:
                return Response({"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        

    def delete(self, request, format=None):
        url = config('TOKEN_VERIFY')
        params = {"token":request.META["HTTP_AUTHORIZATION"]}
        data = requests.post(url, data=params)
        if data.status_code == 200:
            try:
                user = User.objects.get(token=request.META["HTTP_AUTHORIZATION"])
                user.delete()
                return Response({'msg':'Data Deleted'}, status=status.HTTP_200_OK)
            except User.DoesNotExist as e:
                return Response({"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        