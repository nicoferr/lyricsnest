from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from .models import Song
from .forms import SongForm

# Create your views here.
def index(request):
    return render(request, template_name="mylyrics/index.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Connexion automatique après inscription
            return redirect("mylyrics:dashboard")
    else:
        form = UserCreationForm()

    return render(request, "mylyrics/signup.html", { "form": form })

class DashboardView(generic.ListView):
    template_name = "mylyrics/dashboard.html"
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

            return redirect('mylyrics:dashboard')  # ou autre vue
    else:
        form = SongForm()
    return render(request, 'mylyrics/songs/form.html', {'form': form, 'form_action': reverse('mylyrics:create-song')})


@login_required
def edit_song(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            song = form.save(commit=False)
            song.user = request.user
            song.save()

            return redirect('mylyrics:dashboard')  # ou autre vue
    else:
        form = SongForm(instance=song)
    return render(request, 'mylyrics/songs/form.html', {'form': form, 'form_action': reverse('mylyrics:edit-song', args=[song.pk])})

@login_required
def delete_song(request, pk):
    song = get_object_or_404(Song, pk=pk)

    song.delete()

    return redirect('mylyrics:dashboard')  # ou autre vue