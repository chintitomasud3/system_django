from django.urls import path
from . import views

app_name = 'system_info'

urlpatterns = [
    path('', views.system_dashboard, name='dashboard'),
]