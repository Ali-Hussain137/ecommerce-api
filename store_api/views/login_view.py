from http.client import HTTPResponse
from django.shortcuts import render
from django.views import View
import requests
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from store_api.serializers.user_serializer import UserSerializer
from store_api.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json
# from rest_framework import generics
from rest_framework.views import APIView
from decouple import config

class LoginAPI(APIView):
    def post(self, request, format=None):
        print(request.data)
        user = authenticate(email=request.data['email'], password=request.data['password'])
        if user is not None:
            url = config("GETTOKEN")
            params = {"email":request.data['email'], "password":request.data['password']}
            data = requests.post(url, data=params)
            token = json.loads(data.content)
            user.token = token['access']
            user.save()
            return Response({'token':token['access'], 'refresh':token['refresh']}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'not login'})