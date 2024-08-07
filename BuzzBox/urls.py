
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('signup/',views.signup, name='signup'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logut'),
    path('settings/',views.settings, name='settings'),
    path('upload/',views.upload, name='upload'),
    path('like-post/', views.like_post, name='like_post'),
    path('profile/<str:username>', views.profile,name='profile'), 
    path('follow/', views.follow, name='follow'),
    path('search/', views.search, name='search'),
    

]