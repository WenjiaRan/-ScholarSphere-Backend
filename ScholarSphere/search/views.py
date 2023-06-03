from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from article.models import Work
import datetime
from django.db.models import Q
from django.http import HttpResponse, Http404
from article.views import article_get_by_name, article_get_by_id, article_get_by_author
from user.views import user_get_by_name


@csrf_exempt
def advancesearch(request):
    if request.method == 'POST':
        search_date_from = request.POST.get('searchDatefrom', None)
        search_date_to = request.POST.get('searchDateto', None)
        search_type = request.POST.get('searchType', None)
        search_content = request.POST.get('searchContent', None)
        additional_search_conditions = request.POST.get('additionalSearchCondition', [])

        # 构造Q对象
        q_objects = Q()
        if search_date_from and search_date_to:
            q_objects &= Q(send_time__gte=datetime.datetime.fromtimestamp(int(search_date_from))) & \
                         Q(send_time__lte=datetime.datetime.fromtimestamp(int(search_date_to)))
        if search_type and search_content:
            q_objects &= Q(**{search_type + "__icontains": search_content})

        # 处理additionalSearchCondition
        for condition in additional_search_conditions:
            bool_value = condition.get('bool', 'AND')
            type_value = condition.get('searchType', None)
            content_value = condition.get('searchContent', None)
            if bool_value == 'AND' and type_value and content_value:
                q_objects &= Q(**{type_value + "__icontains": content_value})
            elif bool_value == 'OR' and type_value and content_value:
                q_objects |= Q(**{type_value + "__icontains": content_value})
            elif bool_value == 'NOT' and type_value and content_value:
                q_objects &= ~Q(**{type_value + "__icontains": content_value})

        # 查询结果
        results = Work.objects.filter(q_objects)

        # 返回json格式的查询结果
        response_data = {
            'results': [
                {
                    'id': result.id,
                    'work_name': result.work_name,
                    'author_id': result.author_id,
                    'url': result.url,
                    'has_pdf': result.has_pdf,
                    'content': result.content,
                    'send_time': result.send_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'author': result.author,
                    'category': result.category
                } for result in results
            ]
        }
        return JsonResponse(response_data)


@csrf_exempt
def add_work(request):
    if request.method == 'POST':
        data = request.POST
        work = Work(
            open_alex_id=data.get('open_alex_id'),
            work_name=data.get('work_name'),
            author_id=data.get('author_id'),
            url=data.get('url'),
            pdf=request.FILES.get('pdf'),
            has_pdf=int(data.get('has_pdf', 1)),
            content=data.get('content'),
            send_time=data.get('send_time'),
            author=data.get('author'),
            category=data.get('category')
        )
        work.save()
        return JsonResponse({'message': 'Work added successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})



@csrf_exempt
def get_work_pdf(request):
    try:
        data=request.POST
        work = data.get('work_id')
        if work.pdf:
            with work.pdf.open('rb') as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{work.pdf.name}"'
                return response
        else:
            raise Http404('PDF not found.')
    except Work.DoesNotExist:
        raise Http404('Work not found.')


@csrf_exempt
def normal_search(request):
    if request.method == 'POST':
        search_method=request.POST.get('search_method')
        search_key=request.POST.get('search_key')
        if search_method == 'scholar':
            results=user_get_by_name(search_key)
            if results is None:
                result = {'result': 0, 'message': r"未查询到此人！"}
                return JsonResponse(result)
            response_data = {
                'results': [
                    {
                        'id': result.id,
                        'name':result.real_info.name,
                        'email':result.email,
                        'url':result.url
                    } for result in results
                ]
            }

        else:
            search_type=request.POST.get('search_type')
            if search_type == 'article_name':
                results=article_get_by_name(search_key)
            elif search_type == 'article_id':
                results=article_get_by_id(search_key)
            elif search_type == 'author_name':
                results=article_get_by_author(search_key)
            else:
                result = {'result': 0, 'message': r"超出搜索范围！"}
                return JsonResponse(result)
            if results is None:
                result = {'result': 0, 'message': r"未查询到相关文章！"}
                return JsonResponse(result)
            response_data = {
                'results': [
                    {
                        'id': result.id,
                        'work_name': result.work_name,
                        'author_id': result.author_id,
                        'url': result.url,
                        'has_pdf': result.has_pdf,
                        'content': result.content,
                        'send_time': result.send_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'author': result.author,
                        'category': result.category
                    } for result in results
                ]
            }
        return JsonResponse(response_data)
    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
        return JsonResponse(result)