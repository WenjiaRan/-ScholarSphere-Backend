from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

@csrf_exempt    # 跨域设置
def tests(request):
    result = {'result': 1, 'message': r"hello world！"}
    return JsonResponse(result)