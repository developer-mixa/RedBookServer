from django.urls import path
from red_book_server.endpoints import main


REST_BASE = 'rest'

def rest_path(route: str, func, name=None):
    return path(f'{REST_BASE}{route}', func, name=name)

urlpatterns = [
    rest_path('/red_book_info/', main.red_book_info, name='red_book_info')
]