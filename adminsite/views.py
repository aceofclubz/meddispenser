from django.shortcuts import render
from django.http import JsonResponse
from .models import *

# Create your views here.

def requestAjax(reqeust):
    data = {‘is_valid’: False,}
    if request.is_ajax():
        message = request.POST.get(‘message’)
    if message == ‘I want an AJAX response’:
        data.update(is_valid=True)
        data.update(‘response’=’This is the response you wanted’)
    return JsonResponse(data)
