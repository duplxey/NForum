from django import forms
from tinymce import TinyMCE


class PageAddForm(forms.Form):
    display_index = forms.IntegerField(max_value=999)
    title = forms.CharField(max_length=64)
    url = forms.CharField(max_length=64)
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 15}), max_length=5000)


class PageChangeForm(forms.Form):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 15}), max_length=5000)


class PageDeleteForm(forms.Form):
    confirm = forms.BooleanField
