from django.db import models

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

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
