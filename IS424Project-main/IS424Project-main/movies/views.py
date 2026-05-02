from django.shortcuts import render, redirect
from .models import Movie, Rating
from django.db.models import Avg
from .forms import MovieForm
from django.contrib.auth.decorators import login_required

def movie_list(request):
    movies = Movie.objects.annotate(average_rating=Avg('rating__rating'))
    return render(request, 'movies.html', {'movies': movies})


def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)

    ratings = Rating.objects.filter(movie=movie)

    avg_data = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))
    average_rating = avg_data['rating__avg'] or 0
    user_rating = None
    message = ""

    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(movie=movie, user=request.user).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')

        rating_value = request.POST.get("rating")

        if user_rating:
            user_rating.rating = rating_value
            user_rating.save()
            message = "Your rating has been updated!"
        else:
            Rating.objects.create(user=request.user, movie=movie, rating=rating_value)
            message = "Rating submitted successfully!"

    return render(request, 'movie_detail.html', {
    'movie': movie,
    'average_rating': round(average_rating, 1),
    'user_rating': user_rating,
    'ratings': ratings,
    'message': message
})
    


@login_required
def add_movie(request):
    message = ""

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            message = "Movie added successfully!"
            return render(request, 'movie_form.html', {
                'form': MovieForm(),
                'title': 'Add New Movie',
                'message': message
            })
    else:
        form = MovieForm()

    return render(request, 'movie_form.html', {
        'form': form,
        'title': 'Add New Movie',
        'message': message
    })


@login_required
def update_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    message = ""

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            message = "Movie updated successfully!"
            return render(request, 'movie_form.html', {
                'form': form,
                'title': 'Update Movie',
                'message': message
            })
    else:
        form = MovieForm(instance=movie)

    return render(request, 'movie_form.html', {
        'form': form,
        'title': 'Update Movie',
        'message': message
    })


@login_required
def delete_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)

    if request.method == "POST":
        movie.delete()
        movies = Movie.objects.all()
        return render(request, 'movies.html', {
            'movies': movies,
            'message': 'Movie deleted successfully!'
        })

    return render(request, 'movie_delete.html', {'movie': movie})


@login_required
def my_ratings(request):
    ratings = Rating.objects.filter(user=request.user)
    return render(request, 'my_ratings.html', {'ratings': ratings})
