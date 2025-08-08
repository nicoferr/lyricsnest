from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from .models import Song
from .forms import SongForm, GenerateForm
import re
from django.conf import global_settings
from together import Together

TOGETHER_API_URL = "https://api.together.xyz/v1/completions"

# Create your views here.
def index(request):
    return render(request, template_name="lyricsnest/index.html")

def custom_page_not_found_view(request, exception):
    return render(request, "lyricsnest/404.html", status=404)

def invokeAI(prompt):
    client = Together()

    return client.chat.completions.create(
                model="mistralai/Mistral-Small-24B-Instruct-2501", # ou tout autre modèle disponible
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            ).choices[0].message.content.strip()
     

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Connexion automatique après inscription
            return redirect("lyricsnest:dashboard")
    else:
        form = UserCreationForm()

    return render(request, "lyricsnest/signup.html", { "form": form })

class DashboardView(generic.ListView):
    template_name = "lyricsnest/dashboard.html"
    context_object_name = "songs"

    def get_queryset(self):

        songs = Song.objects.filter(created_at__lte=timezone.now(), user=self.request.user).order_by("-created_at")

        return songs
    
@login_required
def create_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.user = request.user
            song.save()

            return redirect('lyricsnest:dashboard')  # ou autre vue
    else:
        form = SongForm()
    return render(request, 'lyricsnest/songs/form.html', {'form': form, 'form_action': reverse('lyricsnest:create-song')})


@login_required
def edit_song(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            song = form.save(commit=False)
            song.user = request.user
            song.save()

            return redirect('lyricsnest:dashboard')  # ou autre vue
    else:
        form = SongForm(instance=song)
    return render(request, 'lyricsnest/songs/form.html', {'form': form, 'form_action': reverse('lyricsnest:edit-song', args=[song.pk])})

@login_required
def delete_song(request, pk):
    song = get_object_or_404(Song, pk=pk)

    song.delete()

    return redirect('lyricsnest:dashboard')  # ou autre vue

@login_required
def import_lyrics(request):
    if(request.method == 'POST'):
        uploaded_file = request.FILES.get('file')

        if uploaded_file and uploaded_file.name.endswith('.txt'):
            title = uploaded_file.name[:-4]
            lyrics = uploaded_file.read().decode('utf-8', errors="replace")

            lyrics = re.sub(r'\n\s*\n+', '\n\n', lyrics)

            Song.objects.create(
                title = title.strip(),
                lyrics = lyrics.strip(),
                user = request.user
            )

    return redirect('lyricsnest:dashboard')

@login_required
def generate(request, pk=None):
    song = None
    if pk:
        song = get_object_or_404(Song, pk=pk)

    form = GenerateForm()
    form.fields['genres'].choices = [
        ('', 'None'),
        ('Country','Country'),
        ('Hip-Hop/Rap','Hip-Hop/Rap'),
        ('Jazz','Jazz'),
        ('Metal','Metal'),
        ('Pop','Pop'),
        ('Pop-Punk','Pop-Punk'),
        ('Punk','Punk'),
        ('R&B/Soul','R&B/Soul'),
        ('Reggae','Reggae'),
        ('Reggaeton','Reggaeton'),
        ('Rock','Rock'),
    ]

    languages = global_settings.LANGUAGES
    sorted_languages = sorted(languages, key=lambda x: x[1].capitalize())
    form.fields['language'].choices = [("", None)] + [(code,name) for code,name in sorted_languages]
    if song:
        form.fields['lyrics'].initial = song.lyrics[:1500]

    response = ""
    ai_lyrics = ""
    ai_title = ""
    if request.method == 'POST':
        prompt = f"""
            You are a song writer. Write lyrics with the following instructions :

            # Instructions

            - Genre : {request.POST.get('genres')} 
            - Lyrics context : {request.POST.get('context')}
            - Lyrics to complete : {request.POST.get('lyrics')}
            - Lyrics language : {request.POST.get('language')}
            - Don't answer anything else other than the lyrics
        """
        ai_lyrics = invokeAI(prompt=prompt)

        title_prompt = f"Find a title for the following lyrics: {ai_lyrics} # Instructions : Don't answer anything else other than the title, without quotes"
        if song and not request.POST.get("generate_title"):
            ai_title = song.title
        else:
            ai_title = invokeAI(title_prompt).replace('"', '')

    return render(request, 'lyricsnest/songs/generate.html', { 'song': song, 'form': form, 'ai_lyrics': ai_lyrics, 'ai_title': ai_title })

@login_required
def save_lyrics(request):
    if request.method == 'POST':
        song = Song(
            title=request.POST.get("title"),
            lyrics=request.POST.get("lyrics")
        )
        song.user = request.user
        song.save()

    return redirect("lyricsnest:dashboard")

@login_required
def edit_lyrics(request, pk):
    if request.method == 'POST':
        song = get_object_or_404(Song, pk=pk)
        song.title = request.POST.get('update-title')
        song.lyrics = request.POST.get('update-lyrics')
        song.user = request.user

        song.save()

    return redirect('lyricsnest:dashboard')