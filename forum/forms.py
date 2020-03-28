from django import forms
from tinymce import TinyMCE

from forum.models import ThreadPrefix


class CreateThreadForm(forms.Form):
    prefix = forms.ModelChoiceField(queryset=ThreadPrefix.objects.all(), required=False)
    title = forms.CharField(label="Thread title", max_length=200)
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 15}), max_length=25000)


class PostReplyForm(forms.Form):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 15}), max_length=25000)


class PostDeleteForm(forms.Form):
    confirm = forms.BooleanField
