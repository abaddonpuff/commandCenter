from django.shortcuts import render,get_object_or_404
from .forms import SubmitXUser
from centralHub.models import TwitterUser, TwitterUserPosts
from .xTwitter.twitterAPI import x_userlookup

# Create your views here.

def submit_x_user(request):
    if request.method == 'POST':
        form_handle = SubmitXUser(request.POST)
        if form_handle.is_valid():
            entered_handle = form_handle.cleaned_data['handle']
            x_api_response = x_userlookup(entered_handle)
            entered_handle, created = TwitterUser.objects.get_or_create(twitter_handle=x_api_response['data']['username'],
                                                        twitter_user_id=x_api_response['data']['id'],
                                                        twitter_handle_avatar='none')
            if not created:
                print(f"Skip, user {entered_handle} already exists")


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