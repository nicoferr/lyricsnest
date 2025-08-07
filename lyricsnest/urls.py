from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name = "lyricsnest"
urlpatterns = [
    path('', views.index, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name="lyricsnest/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="lyricsnest:login"), name="logout"),
    path('dashboard/', login_required(views.DashboardView.as_view()), name="dashboard"),
    path('songs/create/', login_required(views.create_song), name="create-song"),
    path('songs/<int:pk>/edit', login_required(views.edit_song), name="edit-song"),
    path('songs/<int:pk>/delete', login_required(views.delete_song), name="delete-song"),
    path('import/', login_required(views.import_lyrics), name="import"),
    path('generate/', login_required(views.generate), name="generate"),
    path('generate/<int:pk>', login_required(views.generate), name="edit-generate")
]