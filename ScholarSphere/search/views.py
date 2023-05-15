from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from article.models import Work
import datetime
from django.db.models import Q

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