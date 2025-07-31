from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone
from .models import Song

# Create your views here.
def index(request):
    return render(request, template_name="mylyrics/index.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Connexion automatique après inscription
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "mylyrics/signup.html", { "form": form })

# @login_required
# def dashboard(request):

#     return render(request, "mylyrics/dashboard.html")
class DashboardView(generic.ListView):
    template_name = "mylyrics/dashboard.html"
    context_object_name = "songs"

    def get_queryset(self):

        songs = Song.objects.filter(created_at__lte=timezone.now()).order_by("-created_at")

        return songs