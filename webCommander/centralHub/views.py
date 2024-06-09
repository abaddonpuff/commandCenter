from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from centralHub.forms import SubmitXUser, SpotifySearchForm, SpotifyChoicesForm
from centralHub.models import TwitterUser, TwitterUserPosts, SpotifyArtistInfo
from centralHub.spotify.spotifyAPI import search_spotify_artist

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

    print(f'################MY REQUEST METHOD IS {request.method}')
    if request.method == 'POST':
        spotify_search_form = SpotifySearchForm(request.POST)
        if spotify_search_form.is_valid():
            artist_query = spotify_search_form.cleaned_data['artist']
            return render(request, 'spotifyFramework/spotify_summary.html', {'artist_query':artist_query})
    else:
        print("####Im here")
        spotify_search_form = SpotifySearchForm()

    return render(request, 'spotifyFramework/spotify_summary.html',{'allartists':allartists})

def get_artists(request):
    name = request.GET.get("artist", "")
    response = search_spotify_artist(name)

    options = ''.join(
        "<option value='{val}'>{val}, Popularity: {pop}</option>".format(val=row[0], pop=row[2]) for row in response
    )
    return HttpResponse(options)

def get_artists_form(request):
    print(f'################MY REQUEST METHOD IS {request.method}')
    if request.method == 'POST':
        spotify_search_form = SpotifySearchForm(request.POST)
        if spotify_search_form.is_valid():
            artist_query = spotify_search_form.cleaned_data['artist']
            return render(request, 'spotifyFramework/spotify_summary.html', {'artist_query':artist_query})
    else:
        spotify_search_form = SpotifySearchForm()

    return render(request, 'spotifyFramework/spotify_summary.html', {'spotify_search_form':spotify_search_form})

def submit_spotify_artist(request):
    if request.method == 'POST':
        form_handle = SubmitSpotifyArtist(request.POST)
        
    return render(request, 'spotifyFramework/spotify_summary.html',{'form_handle':form_handle})
