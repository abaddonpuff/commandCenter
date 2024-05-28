from django import forms

class SubmitXUser(forms.Form):
    handle = forms.CharField(label="Enter a handle to submit", max_length=20)