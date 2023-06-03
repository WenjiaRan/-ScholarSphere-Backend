
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chat.models import *
import datetime
from user.views import get_standard_time


@csrf_exempt
def send_info(request):
    if request.method == 'POST':
        info=request.POST.get('info')
        sender_email=request.POST.get('sender_email')
        receiver_email = request.POST.get('receiver_email')
        sender=User.objects.filter(email=sender_email).first()
        receiver=User.objects.filter(email=receiver_email).first()
        time_now=get_standard_time(datetime.datetime.now())
        ChatInfo(sender=sender,receiver=receiver,information=info,readCheck=False,sendTime=time_now).save()
        result = {'result': 1, 'message': r"发送成功！"}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
        return JsonResponse(result)

@csrf_exempt
def history_info(request):
    if request.method == 'POST':
        user1_email = request.POST.get('user1_email')
        user2_email= request.POST.get('user2_email')
        user1 = User.objects.filter(email=user1_email).first()
        user2 = User.objects.filter(email=user2_email).first()
        results1=ChatInfo.objects.filter(sender=user1,receiver=user2,readCheck=True)
        results2 = ChatInfo.objects.filter(sender=user2, receiver=user1, readCheck=True)
        results3 = results2.union(results1)
        results3 = results3.order_by('sendTime')
        response_data = {
            'results': [
                {
                    'use1_email' : result.sender.email,
                    'use2_email' : result.receiver.email,
                    'info' : result.information,
                    'time' : result.sendTime
                } for result in results3
            ]
        }
        return JsonResponse(response_data)
    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
        return JsonResponse(result)

@csrf_exempt
def check_new_info(request):
    user1_email = request.POST.get('user1_email')
    user1 = User.objects.filter(email=user1_email).first()
    results1 = ChatInfo.objects.filter(receiver=user1, readCheck=False)
    if results1.exists():
        results2 =results1.values_list('sender__email',flat=True).distinct()
        response_data = {
            'results': [
                {
                    'new_from' : result
                } for result in results2
            ]
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            'results': [
                {
                    'new_from': 'NULL'
                }
            ]
        }
        return JsonResponse(response_data)

@csrf_exempt
def user_read_info(request):
    user1_email = request.POST.get('user1_email')
    user2_email = request.POST.get('user2_email')
    user1 = User.objects.filter(email=user1_email).first()
    user2 = User.objects.filter(email=user2_email).first()
    results1 = ChatInfo.objects.filter(sender=user1,receiver=user2, readCheck=False)
    if results1.exists():
        response_data = {
            'results': [
                {
                    'use1_email': result.sender.email,
                    'use2_email': result.receiver.email,
                    'info': result.information,
                    'time': result.sendTime
                } for result in results1
            ]
        }
        for result in results1 :
            result.readCheck=True
            result.save()

        return JsonResponse(response_data)
    else:
        result = {'result': 0, 'message': r"无新信息"}
        return JsonResponse(result)