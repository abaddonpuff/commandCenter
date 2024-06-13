from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from centralHub.forms import SubmitXUser, SpotifySearchForm, SpotifyChoicesForm
from centralHub.models import TwitterUser, TwitterUserPosts, SpotifyArtistInfo, SpotifyAlbumTracking
from centralHub.spotify.spotifyAPI import search_spotify_artist, search_spotify_artist_by_name, get_artist_albums
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
    handle = get_object_or_404(TwitterUser, twitter_handle=twitter_handle)

    return render(request, 'tweetFramework/handle_summary.html',{'handle':handle})

def home_page(request):
    return render(request, 'home.html')

def list_artist(request):
    allartists = SpotifyArtistInfo.objects.all()
    if request.method == 'POST':
        artist = request.POST["artist"]
        artist_choice = request.POST["artistChoicesContainer"]
        artist_metadata = search_spotify_artist_by_name(artist_choice)
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
        "<option value='{val}'>{val}, Popularity: {pop}</option>".format(val=row[0], pop=row[2]) for row in response
    )
    return HttpResponse(options)

def artist_details(request, spotify_artist):
    '''
    Gets the tracks from an artist
    '''
    artist = get_object_or_404(SpotifyArtistInfo, spotify_artist=spotify_artist)

    print(f'Amount of albums registered: {artist.spotify_artist_albums_registered}')
    albums = SpotifyAlbumTracking.objects.select_related("spotify_user").filter(spotify_user=artist)

    #Is there any way to test what will actually happen on the database before doing so? :/
    #New artist initial DB fill
    if len(albums) == 0:
        artist_albums = get_artist_albums(spotify_artist)
        for item in range(0,len(artist_albums['name'])):
            artist=spotify_artist
            name=artist_albums['name'][item]
            tracks=artist_albums['total_tracks'][item]
            url=artist_albums['images'][item]
            print(f'Artist:{artist}\nName:{name}\nTracks:{tracks}\nurl:{url}')
            created_artist, created = SpotifyAlbumTracking.objects.get_or_create(
                spotify_user=spotify_artist,
                spotify_albums=artist_albums['name'][item],
                number_of_tracks=artist_albums['total_tracks'][item],
                spotify_image_url=artist_albums['images'][item]
            )
            if not created:
                messages.add_message(request, messages.INFO, "Some error.")
            else:
                messages.success(request, 'Artist albums filled')
    elif len(get_artist_albums(spotify_artist)['name'][0]) > len(albums):
        print('MissingAlbums')
        #TODO Analyze the DB for the missing albums (update)
    else:
        print('MissingAlbums')

    return render(request, 'spotifyFramework/spotify_artist_detail.html',{'albums': albums})
