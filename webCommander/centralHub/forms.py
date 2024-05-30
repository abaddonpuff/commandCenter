from django import forms

from centralHub.xTwitter.twitterAPI import x_userlookup, XUserDoesNotExist


class SubmitXUser(forms.Form):
    handle = forms.CharField(label="Enter a handle to submit", max_length=20)

    def clean_handle(self):
        handle = self.cleaned_data["handle"]
        try:
            x_api_response = x_userlookup(handle)
            return x_api_response
        except XUserDoesNotExist as e:
            # this triggers form_handle.is_valid() in views.py to return False
            raise forms.ValidationError("Unrecognized X handle")
