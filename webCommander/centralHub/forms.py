from django import forms
import random

response = {
    "data": {
        "pinned_tweet_id": "1795493485858177510",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1417052605776375813/Jc9RL5o7_normal.jpg",
        "name": "UEFA Champions League",
        "id": "627673190",
        "username": "ChampionsLeague",
    },
    "includes": {
        "tweets": [
            {
                "created_at": "2024-05-28T16:33:00.000Z",
                "id": "1795493485858177510",
                "text": "Every Champions League final since 1993 🧵 \n\n#UCLfinal https://t.co/1EmzTuXa5F",
                "author_id": "627673190",
                "edit_history_tweet_ids": ["1795493485858177510"],
            }
        ]
    },
}
# from centralHub.xTwitter.twitterAPI import x_userlookup, XUserDoesNotExist
from centralHub.xTwitter.twitterAPI import XUserDoesNotExist


def x_userlookup(handle):
    return response
    # raise XUserDoesNotExist


class SubmitXUser(forms.Form):
    handle = forms.CharField(label="Enter a handle to submit", max_length=20)

    def clean_handle(self):
        handle = self.cleaned_data["handle"]
        try:
            x_api_response = x_userlookup(handle)
            return x_api_response
        except XUserDoesNotExist as e:
            raise forms.ValidationError("Unrecognized X handle")
