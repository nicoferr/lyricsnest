from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name = "mylyrics"
urlpatterns = [
    path('', views.index, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name="mylyrics/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="mylyrics:login"), name="logout"),
    path('dashboard/', login_required(views.DashboardView.as_view()), name="dashboard"),
    path('songs/create/', login_required(views.create_song), name="create-song"),
]