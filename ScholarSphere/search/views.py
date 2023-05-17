from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from article.models import Work
import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from article.models import Work
from django.http import HttpResponse, Http404

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




def get_work_pdf(request, work_id):
    try:
        work = Work.objects.get(id=work_id)
        if work.pdf:
            with work.pdf.open('rb') as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{work.pdf.name}"'
                return response
        else:
            raise Http404('PDF not found.')
    except Work.DoesNotExist:
        raise Http404('Work not found.')
