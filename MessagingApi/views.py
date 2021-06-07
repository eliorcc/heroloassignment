from django.shortcuts import render
from MessagingApi import auth
from django.contrib.auth.models import User
from MessagingApi.models import *
import datetime
from django.http import HttpResponse,HttpResponseBadRequest
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import pytz
from django.core import serializers

@csrf_exempt
@require_http_methods(["POST"])
def UserLogin(request):
    username = request.headers['username']
    password = request.headers['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('you have logged in successfully')
    return HttpResponse('check your credentials please')
@csrf_exempt
@require_http_methods(["POST"])
@login_required
def WriteMessage(request):
    from_user = request.user
    try:
        to_user = User.objects.get(username__iexact = request.GET['ToUser'])
    except:
        return HttpResponse('please provide a valid ToUser in the request headers')
    message = Message(Readed = False ,Sender = from_user, Receiver = to_user,Subject=request.GET['Subject'], Message = request.GET['Message'],CreationDate = datetime.datetime.now())
    message.save()
    return HttpResponse('message sent successfully')


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def GetMyUnreadMessages(request):

    messages = Message.objects.filter(Receiver__username__iexact=request.user.username)
    messages = messages.filter(Readed=False)
    if(not messages):
        return HttpResponse('you have no new messages')
    qs_json = serializers.serialize('json', messages, use_natural_foreign_keys=True)
    response = HttpResponse(qs_json, content_type='application/json')
    for message in messages:
        message.Readed = True
        message.save()
    return response




#return one message
@csrf_exempt
@require_http_methods(["GET"])
@login_required
def ReadMessage(request):
    message = Message.objects.filter(Receiver__username__iexact=request.user.username).filter(Readed=False).order_by('CreationDate').first()
    if(message == None):
        return HttpResponse('you have no new messages')
    message.Readed = True
    message.save()
    qs_json = serializers.serialize('json', [message], use_natural_foreign_keys=True)
    response = HttpResponse(qs_json, content_type='application/json')
    return response

@csrf_exempt
@require_http_methods(["DELETE"])
@login_required
def DeleteMessage(request,pk):
    try:
        message_to_delete = Message.objects.get(pk=pk)
    except:
        return HttpResponse('i found no message with this pk')
    if(message_to_delete.Receiver == request.user or message_to_delete.Sender == request.user):
        message_to_delete.delete()
        return HttpResponse('message deleted successfully')

@csrf_exempt
@require_http_methods(["GET"])
@login_required
def GetMyMessages(request):
    messages = Message.objects.filter(Receiver__username__iexact=request.user.username)
    if(not messages):
        return HttpResponse('you have no messages')
    qs_json = serializers.serialize('json', messages, use_natural_foreign_keys=True)
    response = HttpResponse(qs_json, content_type='application/json')
    for message in messages:
        message.Readed = True
        message.save()
    return response


