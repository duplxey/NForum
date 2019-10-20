from django import forms

from wiki.models import WikiPage


class PageAddForm(forms.ModelForm):
    class Meta:
        model = WikiPage
        fields = ['display_index', 'title', 'url', 'content']


class PageChangeForm(forms.ModelForm):
    class Meta:
        model = WikiPage
        fields = ['content']


class PageDeleteForm(forms.Form):
    confirm = forms.BooleanField
