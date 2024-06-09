from django.urls import path, include
from centralHub import views

urlpatterns = [
    path('spotify/allArtists', views.list_artist, name="show_all_artists"),
    path('get_artists_form', views.get_artists_form, name="get_artists_form"),
    path('spotify/submit_artist', views.submit_spotify_artist, name="submit_artist"),
    path('spotify/artists/<str:spotify_artist>', views.get_artists, name="artist_summary"),
    path('artists',views.get_artists, name='get_artists'),
    path('x/allusers', views.list_twitter, name="showalltweets"),
    path('x/xHandles/<str:twitter_handle>', views.handle_summary, name="twitter_handle_summary"),
    path('x/submit_handle/', views.submit_x_user, name='submit_handle'),
    path('',views.home_page, name='home'),
]
