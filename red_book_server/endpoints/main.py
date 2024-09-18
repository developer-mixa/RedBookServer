from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from rest_framework import status
from red_book_server.models.models import RedBookItem, Category, RedBookLocation, RedBookItemRequest
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
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
        except TypeError:
            return HttpResponseBadRequest('There is invalid type!')
        except IntegrityError:
            return HttpResponseBadRequest('This thing is already exists')
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
def request_add_info(request: WSGIRequest):
    red_book_info = RedBookItemDTO.from_json(request.data)
 
    location = None
    location_dto = red_book_info.location

    if location_dto:
        location = RedBookLocation.objects.create(longitude=location_dto.longitude, latitude=location_dto.latitude)

    RedBookItemRequest.objects.create(
        name=red_book_info.name, 
        description=red_book_info.description, 
        image=red_book_info.image,
        count=red_book_info.count, 
        category=Category.objects.get(id=red_book_info.category_id), 
        location=location
    ).save()

    return HttpResponse(status=status.HTTP_201_CREATED)

