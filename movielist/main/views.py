from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Movie
from .forms import *

# Create your views here.

def home(request):
    allMovies = Movie.objects.all()

    context = {
        "movies": allMovies,
    }

    return render(request,'main/index.html', context)


def detail(request, id):
    movie = Movie.objects.get(id=id) #select everyhting from movie where id = id

    context = {
        "movie": movie
    }

    return render(request, 'main/details.html', context)

#add movies to database

def add_movies(request):
    if request.method == "POST":
        form = MovieForm(request.POST or None)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("main:home")
    else:
        form = MovieForm()
    return render(request, 'main/addmovies.html', {"form": form, "controller": "Add Movies"})


#edit movies

def edit_movies(request, id):
    movie = Movie.objects.get(id=id)

#form a check
    if request.method == "POST":
        form = MovieForm(request.POST or None,instance=movie)

        #check if from is valid
        if form.is_valid():
            data = form.save(commit = False)
            data.save()

            #return to home page
            return redirect("main:detail", id)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'main/addmovies.html', {"form": form, "controller": "Edit Movie"})


#delte movie

def delete_movies(request, id):
    movie = Movie.objects.get(id=id)
    movie.delete()
    return redirect("main:home")