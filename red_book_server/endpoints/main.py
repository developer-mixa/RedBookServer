from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from rest_framework import status
from red_book_server.models.models import RedBookItem, Category, RedBookLocation
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from red_book_server.serializers.main import RedBookSerializer
from django.db.models import Q
from json.decoder import JSONDecodeError


def __handle_errors(func):
    def wrapper(request: WSGIRequest, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Category.DoesNotExist as e:
            return HttpResponseBadRequest(str(e))
        except KeyError as e:
            return HttpResponseBadRequest(f'There is no key: {str(e)}')
        except JSONDecodeError:
            return HttpResponseBadRequest('There is Invalid body!')
        except TypeError:
            return HttpResponseBadRequest('There is invalid type!')
    return wrapper

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

@api_view(['POST'])
@__handle_errors
def add_red_book_info(request: WSGIRequest):
    image = request.FILES.get('image', None)
    red_book_info = request.data

    if image:
        category = Category.objects.get(id=red_book_info['category_id'])
        location = None
        location_dto = red_book_info.get('location')
        if location_dto:
            longitude = location_dto['longitude']
            latitude = location_dto['latitude']
            if longitude and latitude:
                location = RedBookLocation.objects.create(longitude=longitude, latitude=latitude)
        RedBookItem.objects.create(
            name=red_book_info['name'], 
            description=red_book_info['description'], 
            image=image, count=red_book_info['count'], 
            category=category, 
            location=location
        ).save()

    return HttpResponse(status=status.HTTP_201_CREATED)

