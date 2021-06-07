from django.shortcuts import render
from django.contrib.auth import authenticate

# Create your views here.
def ReturnUserObject(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    return user
