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

