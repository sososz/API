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

@api_view(['GET', 'PUT'])
def get_by_nick(request, nick):

    try:
        user = User.objects.get(pk=nick)
    except:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':

        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    if request.method == 'PUT':
    
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
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
    
# EDITANDO DADOS

    if request.method == "PUT":

        nickname = request.data['user_nickname']

        update_user = User.objects.get(pk=nickname)

        print(request.data)

        serializer = UserSerializer(updadated_user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

# EDITAR DADOS (PUT)

    if request.method == 'PUT':

        nickname = request.data['user_nickname']

        try:
            update_user = User.objects.get(pk=nickname)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        print(request.data)

        serializer = UserSerializer(update_user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

# DELETAR DADOS (DELETE)

    if request.method == 'DELETE':

        try:
            user_to_delete = User.objects.get(pk=request.data['user_nickname'])
            user_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)