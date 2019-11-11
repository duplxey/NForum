from django import forms
from tinymce import TinyMCE


class CreateThreadForm(forms.Form):
    title = forms.CharField(label="Thread title", max_length=200)
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 15}), max_length=2500)


class PostReplyForm(forms.Form):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 15}), max_length=2500)


class PostDeleteForm(forms.Form):
    confirm = forms.BooleanField
