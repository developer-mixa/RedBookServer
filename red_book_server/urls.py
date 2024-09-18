from django.urls import path
from red_book_server.endpoints import main
from red_book_server.views import red_book_site, upload_image
from django.conf.urls.static import static
from django.conf import settings

REST_BASE = 'rest'

def rest_path(route: str, func, name=None):
    return path(f'{REST_BASE}{route}', func, name=name)

urlpatterns = [
    rest_path('/red_book_info/', main.red_book_info, name='red_book_info'),
    rest_path('/upload_book_info/', main.request_add_info, name='upload_book_info'),
    rest_path('/categories/', main.red_book_categories, name='categories'),
    path('', red_book_site, name='home'),
    path('/upload/', upload_image, name='uploading'),
    path('/add_red_book_info/', main.add_info, name='add_red_book_info'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)