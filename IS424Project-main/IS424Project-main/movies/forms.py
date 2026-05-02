from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'release_year', 'description', 'image']        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
