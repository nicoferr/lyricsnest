from django import forms
from .models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'lyrics']

class GenerateForm(forms.Form):
    genres = forms.ChoiceField(label="Select a musical genre")
    context = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={
            'rows': 10,
            'cols': 40,
            'placeholder': 'Add context to your song: topic, feels, etc... - 500 characters maximum'
        })
    )
    lyrics = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'rows': 10,
            'cols': 40,
            'placeholder': 'If you have lyrics you want to complete, put them here - 1000 characters maximum'
        })
    )