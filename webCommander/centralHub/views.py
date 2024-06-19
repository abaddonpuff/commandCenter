from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.db.utils import IntegrityError
from centralHub.forms import SubmitXUser, SpotifySearchForm, SpotifyChoicesForm
from centralHub.models import TwitterUser, TwitterUserPosts, SpotifyArtistInfo, SpotifyAlbumTracking
from centralHub.spotify.spotifyAPI import search_spotify_artist, search_spotify_artist_by_name, get_artist_albums
from centralHub.xTwitter.twitterAPI import get_all_tweets_from_user
from collections import namedtuple

def submit_x_user(request):
    if request.method == 'POST':
        form_handle = SubmitXUser(request.POST)
        if form_handle.is_valid():
            x_api_response = form_handle.cleaned_data['handle']
            entered_handle, created = TwitterUser.objects.get_or_create(
                twitter_handle=x_api_response['data']['username'],
                twitter_name=x_api_response['data']['name'],
                twitter_user_id=x_api_response['data']['id'],
                twitter_handle_avatar=x_api_response['data']['profile_image_url']
            )
            if not created:
                messages.add_message(request, messages.INFO, "Error: User already exists.")
            else:
                return render(request, 'tweetFramework/x_handle_submission_success.html', {'entered_handle':entered_handle})
    else:
        form_handle = SubmitXUser()
    return render(request, 'tweetFramework/x_handle_submission_form.html',{'form_handle':form_handle})

def list_twitter(request):
    alltweets = TwitterUser.objects.all()


    return render(request, 'tweetFramework/showtweets.html',{'alltweets':alltweets})

def handle_summary(request, twitter_handle):
    user = TwitterUser.objects.get(twitter_handle=twitter_handle)

    posts = user.user_posts.all()
    #TODO If no posts get last 20 posts from user
    # if len(posts) == 0:
    #Change to 0 after DB gets adjusted
    if len(posts) == 2:    
        user_posts = get_all_tweets_from_user(user.twitter_handle, max_results=5)
        breakpoint()

    #TODO If posts are populated, search for the latest twee

    #TODO IF latest Tweet is not the first item, then retrieve all items before latest id

    return render(request, 'tweetFramework/handle_summary.html',{'posts':posts,
                                                                 'user':user})

def home_page(request):
    return render(request, 'home.html')

def list_artist(request):
    allartists = SpotifyArtistInfo.user_posts.all()
    if request.method == 'POST':
        artist = request.POST["artist"]
        artist_choice = request.POST["artistChoicesContainer"]
        artist_metadata = get_spotify_artist_by_id(artist_choice)
        created_artist, created = SpotifyArtistInfo.objects.get_or_create(
                spotify_artist=artist_metadata[0],
                spotify_image=artist_metadata[1],
                spotify_popularity=artist_metadata[2]
            )
        if not created:
            messages.add_message(request, messages.INFO, "Error: Artist already in database.")
        else:
            messages.success(request, 'Artist added successfully')
            return render(request, 'spotifyFramework/spotify_summary.html', {'created_artist':created_artist})


    return render(request,
                  'spotifyFramework/spotify_summary.html',
                  {'allartists':allartists})


def get_artists(request):
    '''
    Used to populate artistChoicesContainer

    '''
    name = request.GET.get("artist", "")
    response = search_spotify_artist(name)
    options = ''.join(
        "<option value='{artist_id}'>{val}, Popularity: {pop}, artist_id: {artist_id}, </option>".format(val=row[0], pop=row[2], artist_id=row[3]) for row in response
    )
    return HttpResponse(options)

def artist_details(request, spotify_artist):
    '''
    Gets the tracks from an artist
    '''
    artist = get_object_or_404(SpotifyArtistInfo, spotify_artist=spotify_artist)
    albums = []

    spotify_artist_albums = get_artist_albums(spotify_artist)
    count = 0
    for artist_album in spotify_artist_albums:
        # assuming api response will be the same,
        # this will not re-insert the same album
        try:
            album, created = SpotifyAlbumTracking.objects.get_or_create(
                spotify_user=artist,
                spotify_albums=artist_album.name,
                number_of_tracks=artist_album.total_tracks,
                spotify_image_url=artist_album.image
            )
            albums.append(album)
        except IntegrityError:
            print(f"x) Album {artist_album.name} already in db for arist, skipping")
            continue

        if created:
            count += 1
            print(f"v) Album {album.spotify_albums} added")
        else:
            print(f"x) Album {album.spotify_albums} already in database")

    if count > 0:
        messages.success(request, f'{count} artist albums added successfully')
    else:
        messages.info(request, 'All albums already in database')

    return render(request, 'spotifyFramework/spotify_artist_detail.html',{'albums': albums})
