from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest


def red_book_site(request: WSGIRequest):
    return render(request, 'index.html')

def upload_image(request: WSGIRequest):
    return render(request, 'upload.html')
