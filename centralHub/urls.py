from django.urls import path, include
from django.contrib.auth import views as auth_views
from centralHub import views


urlpatterns = [
    path('spotify/allArtists', views.list_artist, name="show_all_artists"),
    path('spotify/artists/<str:spotify_artist>', views.artist_details, name="artist_summary"),
    path('artists',views.get_artists, name='get_artists'),
    path('x/allusers', views.list_twitter, name="showalltweets"),
    path('x/xHandles/<str:twitter_handle>', views.handle_summary, name="twitter_handle_summary"),
    path('x/submit_handle/', views.submit_x_user, name='submit_handle'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login')
    path('',views.home_page, name='home'),
]
