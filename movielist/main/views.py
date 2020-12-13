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
    if request.user.is_authenticated:
    
        if request.method == "POST":
            form = MovieForm(request.POST or None)

            if form.is_valid():
                data = form.save(commit=False)
                data.save()
                return redirect("main:home")
        else:
            form = MovieForm()
        return render(request, 'main/addmovies.html', {"form": form, "controller": "Add Movies"})
    else:
        return redirect("main:home")


#edit movies

def edit_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
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

        else:
            return redirect("main:home")

    else:
        return redirect("accounts:login")


#delte movie

def delete_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            movie = Movie.objects.get(id=id)
            movie.delete()
            return redirect("main:home")
        else:
            return redirect("main:home")

    else:
        return redirect("accounts:login")   