from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Rating
from django.db.models import Avg
from django.contrib import messages
from .forms import MovieForm
from django.contrib.auth.decorators import login_required

def movie_list(request):
    movies = Movie.objects.annotate(average_rating=Avg('rating__rating'))
    return render(request, 'movies_list.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    avg_data = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))
    average_rating = avg_data['rating__avg'] or 0
    
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(movie=movie, user=request.user).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.info(request, "Please login to rate movies.")
            return redirect('login')
            
        rating_value = request.POST.get("rating")
        if user_rating:
            user_rating.rating = rating_value
            user_rating.save()
            messages.success(request, "Your rating has been updated!")
        else:
            Rating.objects.create(user=request.user, movie=movie, rating=rating_value)
            messages.success(request, "Rating submitted successfully!")
        return redirect('movie_detail', movie_id=movie.id)

    return render(request, 'movie_detail.html', {
        'movie': movie,
        'average_rating': round(average_rating, 1),
        'user_rating': user_rating
    })
@login_required    
def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies_list')
    else:
        form = MovieForm()
    return render(request, 'movie_form.html', {'form': form, 'title': 'Add New Movie'})
@login_required
def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movie_form.html', {'form': form, 'title': 'Update Movie'})
@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        movie.delete()
        return redirect('movies_list')
    return render(request, 'movie_confirm_delete.html', {'movie': movie})    