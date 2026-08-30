from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def pets_add(request: HttpRequest) -> HttpResponse:
    return render(request, 'pets/pet-add-page.html')
def pets_edit(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'pets/pet-edit-page.html')
def pets_delete(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'pets/pet-delete-page.html')
def pets_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'pets/pet-details-page.html')