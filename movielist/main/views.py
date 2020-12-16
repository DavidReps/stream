from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Avg
from .models import *
from .forms import *

# Create your views here.

def home(request):
    query = request.GET.get("title")
    allMovies = None

    if query:
        allMovies = Movie.objects.filter(name__icontains=query)
    else:
        allMovies = Movie.objects.all()

    context = {
        "movies": allMovies,
    }

    return render(request,'main/index.html', context)


def detail(request, id):
    movie = Movie.objects.get(id=id) #select everyhting from movie where id = id

    reviews = Review.objects.filter(movie = id).order_by("-comment")

    average = reviews.aggregate(Avg("rating"))["rating__avg"]

    if average == None:
        average = 0
    
    average = round(average, 2)


    reviews = Review.objects.filter(movie=id)

    context = {
        "movie": movie,
        "reviews": reviews,
        "average": average,
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

def add_review(request, id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None) 
        if form.is_valid():
            data = form.save(commit=False)
            data.commit = request.POST["comment"] 
            data.rating = request.POST["rating"]
            data.user = request.user
            data.movie = movie
            data.save()
            return redirect("main:detail", id)
        else:
            form = ReviewForm()
        return render(request, 'main/details.html', {"form": form})
    else:
        return redirect("accounts:login")


def edit_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)

        review = Review.objects.get(movie=movie, id=review_id)

        #check if review was done by this user

        if request.user == review.user:
            #grant permission

            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if(data.rating > 10) or (data.rating < 0):
                        error = "out of rating bounds."
                        return render(request, 'main/editreview.html', {"error": error, "form":form})

                    else:
                        data.save()
                        return redirect("main:detail", movie_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html', {"form":form})

        else:
            return redirect("main:detail", movie_id)

    else:
        return redirect("accounts:login")


def delete_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)

        review = Review.objects.get(movie=movie, id=review_id)

        #check if review was done by this user

        if request.user == review.user:
            #grant permission

            review.delete()

        return redirect("main:detail", movie_id)

    else:
        return redirect("accounts:login")