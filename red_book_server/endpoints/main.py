from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from rest_framework import status
from red_book_server.models.models import RedBookItem, Category, RedBookLocation, RedBookItemRequest, RedBookItemBase
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from red_book_server.serializers.main import RedBookSerializer
from django.db.models import Q
from json.decoder import JSONDecodeError
from red_book_server.endpoints.dto import RedBookItemDTO
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


def __handle_errors(func):
    def wrapper(request: WSGIRequest, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Category.DoesNotExist as e:
            return HttpResponseBadRequest(str(e))
        except KeyError as e:
            return HttpResponseBadRequest(f'There is no key: {str(e)}')
        except ValidationError as e:
            return HttpResponseBadRequest(e.message)
        except JSONDecodeError:
            return HttpResponseBadRequest('There is Invalid body!')
        except TypeError as e:
            return HttpResponseBadRequest(f'There is invalid type! {e}')
        except IntegrityError:
            return HttpResponseBadRequest('This thing is already exists')
    return wrapper


def __base_add_info(data, red_book_item_base: RedBookItemBase, success_response):
    red_book_info = RedBookItemDTO.from_json(data)
 
    location = None
    location_dto = red_book_info.location

    if location_dto:
        location = RedBookLocation.objects.create(longitude=location_dto.longitude, latitude=location_dto.latitude)

    red_book_item_base.objects.create(
        name=red_book_info.name, 
        description=red_book_info.description, 
        image=red_book_info.image,
        count=red_book_info.count, 
        category=Category.objects.get(id=red_book_info.category_id), 
        location=location
    ).save()

    return success_response

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
def request_add_info(request: WSGIRequest):
    return __base_add_info(request.data, RedBookItemRequest, HttpResponse(status=status.HTTP_201_CREATED))

@api_view(['POST'])
@__handle_errors
def add_info(request: WSGIRequest):

    # There was no time to think about better conditions :(

    id = request.POST.get('id')

    data = {
    'name': request.POST.get('name'),
    'description': request.POST.get('description'),
    'category_id': request.POST.get('category_id'),
    'longitude': request.POST.get('longitude'),
    'latitude': request.POST.get('latitude'),
    'image': request.POST.get('image'),
    'count': request.POST.get('count')
    }

    response = __base_add_info(data, RedBookItem, HttpResponseRedirect(request.META.get('HTTP_REFERER')))

    RedBookItemRequest.objects.get(id=id).delete()

    return response
