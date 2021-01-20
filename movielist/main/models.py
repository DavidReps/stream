from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Movie(models.Model):
    #fields for movie table
    #TODO add vote fields
    #TODO add different platforms
    name = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    release_date = models.DateField()
    rating = models.FloatField(default=0)
    image = models.URLField(default=None, null=True)

    netflix = models.IntegerField(default=0)
    hulu = models.IntegerField(default=0)
    amazon = models.IntegerField(default=0)
    youtube = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=0)
    
    netflix = models.IntegerField(default=0)
    hulu = models.IntegerField(default=0)
    amazon = models.IntegerField(default=0)
    youtube = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username