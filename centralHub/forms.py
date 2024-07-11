from django import forms
from django.contrib.auth.forms import AuthenticationForm
from centralHub.xTwitter.twitterAPI import (
    x_userlookup,
    XUserDoesNotExist,
    XAPIUsageExceeded,
)


class SubmitXUser(forms.Form):
    handle = forms.CharField(label="Enter a handle to submit", max_length=20)

    def clean_handle(self):
        handle = self.cleaned_data["handle"]
        try:
            x_api_response = x_userlookup(handle)
            return x_api_response
        except XUserDoesNotExist:
            raise forms.ValidationError("Unrecognized X handle")
        except XAPIUsageExceeded:
            raise forms.ValidationError(f"API Usage exceeded to query handle {handle}")


class SpotifySearchForm(forms.Form):
    artist = forms.CharField(label="Search for an artist", max_length=100)


class SpotifyChoicesForm(forms.Form):
    artist_choices = forms.ChoiceField(label="Select your option", choices=[])


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"
