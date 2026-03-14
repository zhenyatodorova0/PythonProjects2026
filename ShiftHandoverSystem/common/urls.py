from django.urls import path
from common.views import GlobalSearchView, current_time

app_name = 'common'

urlpatterns = [
    path('current_time/', current_time, name='current_time'),
    path('search/', GlobalSearchView.as_view(), name='search'),
]
