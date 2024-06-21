from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.db.utils import IntegrityError
from centralHub.forms import SubmitXUser
from centralHub.models import TwitterUser, TwitterUserPosts, SpotifyArtistInfo, SpotifyAlbumTracking
from centralHub.spotify.spotifyAPI import search_spotify_artist, get_artist_albums, get_spotify_artist_by_id
from centralHub.xTwitter.twitterAPI import get_top_tweets_from_user, get_tweets_since_last

FIRST_LOAD=20

def submit_x_user(request):
    if request.method == 'POST':
        form_handle = SubmitXUser(request.POST)
        if form_handle.is_valid():
            x_api_response = form_handle.cleaned_data['handle']
            entered_handle, created = TwitterUser.objects.get_or_create(
                twitter_handle=x_api_response['data']['username'],
                twitter_name=x_api_response['data']['name'],
                twitter_user_id=x_api_response['data']['id'],
                twitter_handle_avatar=x_api_response['data']['profile_image_url'],
                twitter_last_post_id=x_api_response['data']['most_recent_tweet_id']
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

def insert_to_x_db(twitter_user, tweet_data):
    created_count=0
    for tweet in tweet_data['data']:
        created_tweet, created = TwitterUserPosts.objects.get_or_create(
                    twitter_user = twitter_user,
                    #TODO create a function to obtain the post type if containing media
                    twitter_post_type = 'text',
                    twitter_post_id = tweet['id'],
                    twitter_text = tweet['text'],
                    twitter_post_to_link = f"https://x.com/{twitter_user.twitter_handle}/status/{tweet['id']}"
                )
        if created:
            created_count += 1
            twitter_user.twitter_last_post_id = tweet_data['meta']['newest_id']
        return created_count

def handle_summary(request, twitter_handle):
    user = TwitterUser.objects.get(twitter_handle=twitter_handle)

    posts = user.user_posts.all()
    created_count = 0

    if posts.count() == 0:
        last_tweets = get_top_tweets_from_user(user.twitter_handle, max_results=FIRST_LOAD)
        created_count = insert_to_x_db(user, last_tweets)
        #TODO If posts are populated, search for the latest tweet
    else:
        new_posts = get_tweets_since_last(user.twitter_user_id,user.twitter_last_post_id)
        if 'data' in new_posts.keys():
            #New items introduced
            created_count= insert_to_x_db(user, new_posts)

    if created_count > 0:
        messages.success(request, f'{created_count} Posts created')

    #TODO IF latest Tweet is not the first item, then retrieve all items before latest id
    return render(request, 'tweetFramework/handle_summary.html',{'posts':posts, 'user':user})


def home_page(request):
    return render(request, 'home.html')

def list_artist(request):
    allartists = SpotifyArtistInfo.objects.all()
    if request.method == 'POST':
        artist_choice = request.POST["artistChoicesContainer"]
        artist_metadata = get_spotify_artist_by_id(artist_choice)
        created_artist, created = SpotifyArtistInfo.objects.get_or_create(
                spotify_artist=artist_metadata['name'],
                spotify_image=artist_metadata['images'][0]['url'],
                spotify_popularity=artist_metadata['popularity'],
                spotify_artist_id=artist_metadata['id']
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
        "<option value='{artist_id}'>{val}, Popularity: {pop} </option>".format(val=row[0], pop=row[2], artist_id=row[3]) for row in response
    )
    return HttpResponse(options)

def artist_details(request, spotify_artist):
    '''
    Gets the tracks from an artist
    '''
    artist = get_object_or_404(SpotifyArtistInfo, spotify_artist=spotify_artist)
    albums = []

    spotify_artist_albums = get_artist_albums(artist.spotify_artist_id)
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
