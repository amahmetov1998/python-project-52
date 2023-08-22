from django.urls import path
from .views import *

urlpatterns = [
    path('', ShowUsers.as_view(), name='users'),
    path('<int:pk>/update/', UpdateUser.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteUser.as_view(), name='delete'),
    path('create/', RegisterUser.as_view(), name='register'),
    # path('statuses/', name='statuses'),
    # path('labels/', name='labels'),
    # path('tasks/', name='tasks'),
]
