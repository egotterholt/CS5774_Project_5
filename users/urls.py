from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    # library views
    # path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/<str:username>/items', views.profile_items, name='profile-items'),
    path('profile/<str:username>/edit', views.profile_edit, name='profile-edit'),
    path('profile/<str:username>/delete', views.profile_delete, name='profile-delete'),
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
]