from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_dashboard, name='dashboard'),
    path('partial/', views.task_list_partial, name='list_partial'),
    path('partial/stats/', views.task_stats_partial, name='stats_partial'),
    path('create/', views.task_create, name='create'),
    path('<int:pk>/edit/', views.task_edit, name='edit'),
    path('<int:pk>/update-status/', views.task_update_status, name='update_status'),
    path('<int:pk>/delete/', views.task_delete, name='delete'),
    path('<int:pk>/detail/', views.task_detail, name='detail'),
]
