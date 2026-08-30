from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def photo_add(request: HttpRequest) -> HttpResponse:
    return render(request, 'pets/pet-add-page.html')
def photo_edit(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'pets/pet-edit-page.html')
def photo_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'pets/pet-details-page.html')