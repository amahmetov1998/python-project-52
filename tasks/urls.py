from django.urls import path


from .views import *


urlpatterns = [
    path('', ShowTasks.as_view(), name='tasks'),
    path('<int:pk>/update/', UpdateTask.as_view(), name='update_task'),
    path('<int:pk>/delete/', DeleteTask.as_view(), name='delete_task'),
    path('<int:pk>/', ViewTask.as_view(), name='view_task'),
    path('create/', CreateTask.as_view(), name='create_task'),
]
