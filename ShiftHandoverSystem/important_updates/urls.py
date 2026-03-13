from django.urls import path
from important_updates import views

app_name = 'important_updates'

urlpatterns = [
    path('', views.UpdateListView.as_view(), name='list'),
    path('create/', views.UpdateCreateView.as_view(), name='create'),
    path('details/<int:pk>/', views.UpdateDetailView.as_view(), name='update-details'),
    path('edit/<int:pk>/', views.UpdateEditView.as_view(), name='update-edit'),
    path('<int:pk>/delete/', views.UpdateDeleteView.as_view(), name='update-delete'),
]
