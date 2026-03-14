from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movies_list'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('add/', views.add_movie, name='add_movie'),
    path('update/<int:movie_id>/', views.update_movie, name='update_movie'),
    path('delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
]