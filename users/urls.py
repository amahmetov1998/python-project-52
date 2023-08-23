from django.urls import path
from .views import *

urlpatterns = [
    path('', ShowUsers.as_view(), name='users'),
    path('<int:pk>/update/', UpdateUser.as_view(), name='update_user'),
    path('<int:pk>/delete/', DeleteUser.as_view(), name='delete_user'),
    path('create/', RegisterUser.as_view(), name='register_user'),
]
