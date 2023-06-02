from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('', index, name='index'),
    path('post/<int:id>/', posting, name='posting'),
    path('update_blog/<int:id>', update_blog, name='update_blog'),
    path('delete_blog/<int:id>', delete_blog, name='delete_blog'),
    path('profile/', user_profile, name='profile'),
    path('update_profile/', update_profile.as_view(), name='update_profile'),
    path('create/',create_post,name='post')
]
