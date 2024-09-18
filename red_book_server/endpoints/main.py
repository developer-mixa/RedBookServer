from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from red_book_server.models.models import RedBookItem, Category
from django.http import JsonResponse
from red_book_server.serializers.main import RedBookSerializer
from django.db.models import Q


@api_view(['GET'])
def red_book_info(request: WSGIRequest):
    red_book_items = RedBookItem.objects.all()
    categories = request.GET.getlist('categories', default=None)
    name = request.GET.get('name', default=None)
    offset = int(request.GET.get('offset', default=0))
    limit = int(request.GET.get('limit', 100))

    red_book_items = RedBookItem.objects.select_related(
        'category'
    ).filter(
        category__isnull=False,
        category__id__in=categories if categories else Q(),
        name__istartswith=name if name else Q()
    )[offset:limit + offset]

    return JsonResponse(RedBookSerializer(red_book_items, many=True).data, safe=False)