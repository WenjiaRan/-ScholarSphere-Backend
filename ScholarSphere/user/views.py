# publish/views.py
import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from user.models import *


def check_number(password):
    for c in password:
        if c.isnumeric():
            return True


def check_letter(password):
    for c in password:
        if 'a' <= c <= 'z' or 'A' <= c <= 'Z':
            return True


def check_mark(password):
    for c in password:
        if not (c.isnumeric() or 'a' <= c <= 'z' or 'A' <= c <= 'Z'):
            return True
def check_legal(password):
    if len(password) < 8 or len(password) > 16:
        return {'result': 0, 'message': '长度需为8-16个字符,请重新输入。'}
    else:
        for i in password:
            if 0x4e00 <= ord(i) <= 0x9fa5 or ord(i) == 0x20:  # Ox4e00等十六进制数分别为中文字符和空格的Unicode编码
                return {'result': 0, 'message': '不能使用空格、中文，请重新输入。'}
        else:
            key = 0
            key += 1 if check_number(password) else 0
            key += 1 if check_letter(password) else 0
            key += 1 if check_mark(password) else 0
            if key >= 2:
                return {'result': 1, 'message': '密码强度合适'}
            else:
                return {'result': 0, 'message': '至少含数字/字母/字符2种组合，请重新输入。'}

def check_password(email,password):
    if User.objects.filter(email=email, password=password).exists():
        return True
    return False

def check_password_wrong_45times(email):
    user = User.objects.filter(email=email).first()
    if user.times_of_wa_password==5:
        user.times_of_wa_password=0
        user.save()
        return True
    user.times_of_wa_password=user.times_of_wa_password+1
    user.save()
    return False


@csrf_exempt    # 跨域设置
def register(request):
    """
    :param request: 请求体
    :return:        1 - 成功， 0 - 失败
    请求体包含包含 password1，password2，email
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) == 0 or len(password2) == 0 or len(email) == 0:
            result = {'result': 0, 'message': r'用户名, 邮箱, 与密码不允许为空!'}
            return JsonResponse(result)

        if User.objects.filter(email=email).exists():
            result = {'result': 0, 'message': r'该邮箱已被注册'}
            return JsonResponse(result)

        if password1 != password2:
            result = {'result': 0, 'message': r'两次密码不一致!'}
            return JsonResponse(result)

        message = check_legal(password1)

        user = User( email=email, password=password1)
        user.save()
        result = {'result': 1, 'message': r"注册成功!"}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
        return JsonResponse(result)

@csrf_exempt
def checkmailregistered(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            result = {'result': 0, 'message': r'该邮箱已被注册!'}
            return JsonResponse(result)
        result = {'result': 1, 'message': r"新邮箱,可以注册!"}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
        return JsonResponse(result)

def check_accessible(user):
    date = user.forbiden_start_time
    if date is None:
        return True
    now = get_standard_time(datetime.datetime.now())
    if date.day<now.day:
        user.forbiden_start_time=None
        user.save()
        return True
    return False

def get_standard_time(time):
    time_str=time.strftime("%Y-%m-%d %H:%M:%S")
    new_time=datetime.datetime.strptime(time_str,"%Y-%m-%d %H:%M:%S")
    return new_time

def check_autologin(user):
    date=user.sevendays_autologin_start_time
    if date is None:
        return False
    now=get_standard_time(datetime.datetime.now())
    if (now-date).days >= 7:
        user.sevendays_autologin_start_time=None
        user.save()
        return False
    return True

@csrf_exempt    # 跨域设置
def login(request):
    """
    :param request: 请求体
    :return:        1 - 成功， 0 - 失败
    请求体包含包含 email，password
    """
    if request.method == 'POST':

        email = request.POST.get('email', '')
        if len(email) == 0:
            result = {'result': 0, 'message': r'邮箱不允许为空!'}
            return JsonResponse(result)

        user = User.objects.filter(email=email)
        if not user.exists():
            result = {'result': 0, 'message': r'用户不存在!'}
            return JsonResponse(result)

        if check_autologin(user.first()):
            result = {'result': 1, 'message': r'登录成功!'}
            return JsonResponse(result)

        if check_accessible(user.first()):
            password = request.POST.get('password', '')
            if len(password)==0:
                result = {'result': 0, 'message': r'密码不能为空!'}
                return JsonResponse(result)
            if not check_password(email,password):
                if check_password_wrong_45times(email):
                    user.update(forbiden_start_time=get_standard_time(datetime.datetime.now()))
                    user.first().save()
                    result = {'result': 0, 'message': r'错误太多，禁止登录!'}
                    return JsonResponse(result)
                result = {'result': 0, 'message': r'密码错误!'}
                return JsonResponse(result)
            else:
                result = {'result': 1, 'message': r'登录成功!'}
                return JsonResponse(result)

        else:
            result = {'result': 0, 'message': r'现在禁止登录!'}
            return JsonResponse(result)

    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
        return JsonResponse(result)

@csrf_exempt    # 跨域设置
def autologin(request):
    """
    :param request: 请求体
    :return:        1 - 成功， 0 - 失败
    请求体包含包含 email
    """
    if request.method == 'POST':
        email = request.POST.get('email', '')
        user = User.objects.filter(email=email).first()
        if user.sevendays_autologin_start_time is None:
            user.sevendays_autologin_start_time = get_standard_time(datetime.datetime.now())
        else:
            user.sevendays_autologin_start_time = None
        user.save()
        result = {'result': 1, 'message': r"设置成功！"}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
        return JsonResponse(result)

def user_get_by_name(user_name):
    return User.objects.filter(real_info__name=user_name, has_real_info=True)

@csrf_exempt
def real_info_set(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            user=user.first()
        else:
            result = {'result': 0, 'message': r"用户不存在"}
            return JsonResponse(result)
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        id_num=request.POST.get('id_num')
        if RealInformation.objects.filter(id_num=id_num).exists():
            result = {'result': 0, 'message': r"此信息已被实名！"}
            return JsonResponse(result)
        real_create=RealInformation(name=name,phone=phone,id_num=id_num)
        real_create.save()
        user.real_info=real_create
        user.has_real_info=True
        user.save()
        result = {'result': 1, 'message': r"实名成功！"}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
        return JsonResponse(result)

@csrf_exempt  # 跨域设置
def change_info(request):
    if request.method == 'POST':
        key_list = request.POST.get('keys')
        val_list = request.POST.get('vals')
        used_password = request.POST.get('used_password')
        email = request.POST.get('email')
        key_list = re.findall(r'"(.*?)"', key_list)
        val_list = re.findall(r'"(.*?)"', val_list)
        if used_password is not None:
            user=User.objects.filter(email=email, password=used_password)
            if not user.exists():
                result = {'result': 0, 'message': r"邮箱密码不匹配"}
                return JsonResponse(result)
        else:
            user=User.objects.filter(email=email)
            if not user.exists():
                result = {'result': 0, 'message': r"用户不存在"}
                return JsonResponse(result)

        if key_list is None or val_list is None:
            result = {'result': 0, 'message': r"未收到修改内容！"}
            return JsonResponse(result)

        kv_dict = dict(zip(key_list, val_list))
        user_result=user.first()
        for key, value in kv_dict.items():
            setattr(user_result, key, value)
        user_result.save()
        result = {'result': 1, 'message': r"修改成功"}
        return JsonResponse(result)

    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
        return JsonResponse(result)

@csrf_exempt  # 跨域设置
def show_self_info(request):
    if request.method == 'POST':
        email=request.get('email')
        result=User.objects.filter(email=email).first()
        if result.has_real_info:
            response_data = {
                'results': [
                    {
                        'password': result.password,
                        'email': result.email,
                        'has_real_info': result.has_real_info,
                        'description' : result.description,
                        'url': result.url,
                        'name':result.real_info.name,
                        'phone':result.real_info.phone,
                        'id_num':result.real_info.id_num
                    }
                ]
            }
        else:
            response_data = {
                'results': [
                    {
                        'password': result.password,
                        'email': result.email,
                        'has_real_info': result.has_real_info,
                        'description': result.description,
                        'url': result.url
                    }
                ]
            }
        return JsonResponse(response_data)
    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
        return JsonResponse(result)