

from django.urls import path
from .views import register_user, user_login, user_logout,upload_image,upload_file,get_image

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('upload_image/',upload_image, name='upload_image'),
    path('upload/',upload_file, name='upload_file'),    
    path('get_image/<int:id>/',get_image, name='get_image'),
]