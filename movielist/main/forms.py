from django import forms
from .models import *

#movie add form

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        #what we ask of user to fill in
        fields = ('name', 'director', 'description', 'release_date', 'image')