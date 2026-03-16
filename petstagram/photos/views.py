from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def photo_add(request: HttpRequest) -> HttpResponse:
    return render(request, 'photos/photo-add-page.html')

def photo_edit(request: HttpRequest) -> HttpResponse:
    return render(request, 'photos/photo-edit-page.html')
def photo_details(request: HttpRequest) -> HttpResponse:
    return render(request, 'photos/photo-details-page.html')
