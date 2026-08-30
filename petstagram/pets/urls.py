

from django.urls import path, include

from pets import views

app_name = 'pets'
urlpatterns = [
    path('add/', views.pets_add, name='add'),
    path('<str:username>/pet/<slug:pet_slug>/', include([
        path('', views.pets_details, name='details'),
        path('edit/', views.pets_edit, name='edit'),
        path('delete/', views.pets_delete, name='delete'),
    ]
    )
         )

]