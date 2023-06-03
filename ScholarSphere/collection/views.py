from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Collection

@csrf_exempt
def add_to_collection(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        work_id = request.POST.get('work_id')

        # 校验work_id和user_id不用写了
        new_collection = Collection(work_id=work_id, user_id=user_id)
        new_collection.save()

        return JsonResponse({'status': 'success'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=400)


@csrf_exempt
def show_collection(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')

        collection_items = Collection.objects.filter(user_id=user_id)
        collection_list = list(collection_items.values())

        return JsonResponse(collection_list, safe=False)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=400)
