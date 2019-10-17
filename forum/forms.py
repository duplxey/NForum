from django import forms


class CreateThreadForm(forms.Form):
    title = forms.CharField(label="Thread title", max_length=200, required=True)
    content = forms.CharField(label="Message", max_length=2500, widget=forms.Textarea, required=True)


class PostReplyForm(forms.Form):
    content = forms.CharField(label="Message", max_length=2500, widget=forms.Textarea)
