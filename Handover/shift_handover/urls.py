from django.urls import path
from shift_handover import views

app_name = 'shift_handover'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-post/', views.add_post, name='add_post'),
]