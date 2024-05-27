from django.shortcuts import render,get_object_or_404
from centralHub.models import TwitterUser

# Create your views here.
def list_twitter(request):
    alltweets = TwitterUser.objects.all()

    return render(request, 'tweetFramework/showtweets.html',{'alltweets':alltweets})

def handle_summary(request, twitter_handle):
    handle = get_object_or_404(TwitterUser, twitter_handle=twitter_handle)

    return render(request, 'tweetFramework/handle_summary.html',{'handle':handle}) 