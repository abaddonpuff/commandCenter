from django.shortcuts import render
from centralHub.models import TwitterFramework

# Create your views here.
def list_twitter(request):
    alltweets = TwitterFramework.objects.all()

    return render(request, 'tweetFramework/showtweets.html',{'alltweets':alltweets})

def handle_summary(request, requested_handle):
    handle = get_object_or_404(TwitterFramework, twitter_handle=requested_handle)

    return render(request, 'tweetFramework/handle_summary.html',{'handle':handle}) 