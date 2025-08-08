from django import forms
from .models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'lyrics']

class GenerateForm(forms.Form):
    context = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 40,
            'resize': 'none',
            'placeholder': 'Add context to your song: topic, feels, etc... - 500 characters maximum',
            'style': 'resize: none;',
            'class': 'border-1 border-gray-200 p-2',
        })
    )
    language = forms.ChoiceField(
        required = False,
        label = "Select a language (optional)",
        widget=forms.Select(attrs={
            'class': 'border-1 border-gray-200 p-2'
        })
    )
    genres = forms.ChoiceField(
        required = False,
        label="Select a musical genre (optional)",
        widget=forms.Select(attrs={
            'class': 'border-1 border-gray-200 p-2'
        })
    )
    generate_title = forms.BooleanField(
        label="Generate title ? (optional)",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'mx-3'
        })
    )
    lyrics = forms.CharField(
        label="Lyrics (optional)",
        required=False,
        max_length=1500,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 40,
            'resize': 'none',
            'placeholder': 'If you have lyrics you want to complete, put them here - 1500 characters maximum',
            'style': 'resize: none;',
            'class': 'border-1 border-gray-200 p-2',
        })
    )