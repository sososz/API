from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer

import json

@api_view(['GET'])
def get_users(request):

    if request.method == 'GET':

        users = User.objects.all()                # Get all objects in User's database (It returns a queryset)

        serializer = UserSerializer(users, many=True)   # Serialize the object data into json (Has a 'nany' parameter cause it's a queryset)

        return Response(serializer.data)   # Return the serialized data 
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_by_nick(request, nick):

    try:
        user = User.objects.get(pk=nick)
    except:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':

        serializer = UserSerializer(user)
        return Response(serializer.data)
    
#CRUD
@api_view(['GET','POST','DELETE'])
def user_manager(request):

    if request.method == 'GET':
            
        try:
            if request.GET['user']:

                user_nickname = request.GET['user']

                try:
                    user = User.objects.get(pk=user_nickname)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                
                serializer = UserSerializer(user)
                return Response(serializer.data)
                
            else: 
                return Response(status=status.HTTP_400_BAD_REQUEST)
                
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Criando dados

    if request.method == 'POST':

        new_user = request.data

        serializer = UserSerializer(data=new_user)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)