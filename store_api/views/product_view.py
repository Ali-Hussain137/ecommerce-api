from http.client import HTTPResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from store_api.serializers.product_serializer import ProductSerializer
from store_api.serializers.image_serializer import ImageSerializer
from store_api.models import Product, User
from store_api.models import Image
import requests
from rest_framework.views import APIView
from decouple import config
import json
from store_api.utility.authorization import UserAuthentication


class ProductAPI(APIView):

    def post(self, request, pk=None, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=pk)
            # for image in request.data.get("images"):
            #     print(image)
            imgserializer = ImageSerializer(data=request.data)
            if imgserializer.is_valid():
                imgserializer.save(product_id=serializer.data['id'])
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        if pk is not None:
            try:
                product = Product.objects.get(pk=pk)
                serializer = ProductSerializer(product)
                images = Image.objects.filter(product_id=product.id)
                imgserializer = ImageSerializer(images, many=True)
                data = {'product':serializer.data, 'images':imgserializer.data}
            except Product.DoesNotExist as e:
                return Response({"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)    
            return Response(data ,status=status.HTTP_200_OK)

        products = Product.objects.all()
        data = {}
        for product in products:
            serializer = ProductSerializer(product)
            images = Image.objects.filter(product_id=product.id)
            imgserializer = ImageSerializer(images, many=True)
            product_data = {'product':serializer.data, 'images':imgserializer.data}
            data[product.id] = product_data
        return Response(data ,status=status.HTTP_200_OK)


    def put(self, request, pk, format=None):
        url = config('TOKEN_VERIFY')
        params = {"token":request.META["HTTP_AUTHORIZATION"]}
        data = requests.post(url, data=params)
        if data.status_code == 200:
            try:
                user = User.objects.get(token=request.META["HTTP_AUTHORIZATION"])
                product = Product.objects.get(pk=pk, user_id=user.id)
                serializer = ProductSerializer(product, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'Complete Data Updated'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist as e:
                return Response({"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        data = requests.post(config('TOKEN_VERIFY'), data={"token":request.META["HTTP_AUTHORIZATION"]})
        if data.status_code == 200:
            try:
                user = User.objects.get(token=request.META["HTTP_AUTHORIZATION"])
                product = Product.objects.get(pk=pk, user_id=user.id)
                product.delete()
                return Response({'msg':'Data Deleted'}, status=status.HTTP_200_OK)
            except User.DoesNotExist as e:
                return Response({"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED) 
        else:
            return Response({"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)



        

    


