from django.urls import path
from . import views

urlpatterns = [
 path('', views.index, name='index'),
path('login/', views.loginV, name="login"),
path('signUp/', views.signUp, name="signUp"),
path('logout/', views.logoutV, name="logout"),
]