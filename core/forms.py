# core/forms.py
from django import forms



class AnimeSearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control mr-sm-2',
            'type': 'search',
            'placeholder': 'Search',
            'aria-label': 'Search',
        })
    )

