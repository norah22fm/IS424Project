from django.urls import path
from . import views

urlpatterns = [
 path('', views.index, name='index'),
 path('login/', views.loginV, name="login"),
 path('signUp/', views.signUp, name="signUp"),
 path('logout/', views.logoutV, name="logout"),
 path('movies/', views.movies, name='movies'),
 path('add_movie/', views.add_movie, name='add_movie'),
]