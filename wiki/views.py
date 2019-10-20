from django.shortcuts import render, redirect
import re

from django.utils import timezone

from wiki.forms import PageAddForm, PageChangeForm, PageDeleteForm
from .models import WikiPage


def index_view(request):
    return page_view(request, 'wiki-index')


def page_view(request, url):
    passed = dict()

    try:
        wiki_page = WikiPage.objects.get(url=url)
    except WikiPage.DoesNotExist:
        return render(request, 'layout/message.html', {
            'message_type': "error",
            'message_title': "Unknown wiki page!",
            'message_content': "The specified wiki page could not be found."
        })

    passed['wiki_page'] = wiki_page

    wiki_pages = WikiPage.objects.all().order_by('display_index')
    passed['wiki_pages'] = wiki_pages

    try:
        next_wiki_page = WikiPage.objects.get(display_index=wiki_page.display_index + 1)
        passed['next_wiki_page'] = next_wiki_page
    except WikiPage.DoesNotExist:
        passed['next_wiki_page'] = None

    try:
        previous_wiki_page = WikiPage.objects.get(display_index=wiki_page.display_index - 1)
        passed['previous_wiki_page'] = previous_wiki_page
    except WikiPage.DoesNotExist:
        passed['previous_wiki_page'] = None

    if request.user.is_authenticated:
        permissions = {
            'add': request.user.has_perm('wiki.add_wikipage'),
            'change': request.user.has_perm('wiki.change_wikipage'),
            'delete': request.user.has_perm('wiki.delete_wikipage'),
        }
        passed['user_permissions'] = permissions

    return render(request, 'wiki/view.html', passed)


def page_add(request):
    if request.user.is_authenticated:
        if not request.user.has_perm('wiki.add_wikipage'):
            return render(request, 'layout/message.html', {
                'message_type': "error",
                'message_title': "Insufficient permissions.",
                'message_content': "You don't have the permission to do that!"
            })
        if request.method == 'POST':
            form = PageAddForm(request.POST)
            if form.is_valid():
                display_index = form.cleaned_data['display_index']
                title = form.cleaned_data['title']
                url = re.sub('[^A-z0-9-_]', "", form.cleaned_data['url']).lower()
                content = form.cleaned_data['content']

                if WikiPage.objects.filter(display_index=display_index).exists():
                    form.add_error('display_index', "Page with this display index already exists!")

                if WikiPage.objects.filter(title=title).exists():
                    form.add_error('title', "Page with this title already exists!")

                if WikiPage.objects.filter(url=url).exists():
                    form.add_error('url', "Page with this url already exists!")

                if form.has_error('display_index') or form.has_error('title') or form.has_error('url'):
                    return render(request, 'wiki/add.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': form})

                page = WikiPage.objects.create(display_index=display_index, title=title, url=url, content=content, author=request.user)
                page.save()

                return redirect('wiki-page', url=url)
            else:
                return render(request, 'wiki/add.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': form})
        else:
            return render(request, 'wiki/add.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': PageAddForm()})
    else:
        return render(request, 'layout/message.html', {
            'message_type': "error",
            'message_title': "Not logged in!",
            'message_content': "You need to be logged in in order to do that."
        })


def page_change(request, url):
    if request.user.is_authenticated:
        if not request.user.has_perm('wiki.change_wikipage'):
            return render(request, 'layout/message.html', {
                'message_type': "error",
                'message_title': "Insufficient permissions.",
                'message_content': "You don't have the permission to do that!"
            })
        if WikiPage.objects.filter(url=url).exists():
            if request.method == 'POST':
                form = PageChangeForm(request.POST)
                if form.is_valid():
                    content = form.cleaned_data['content']

                    page = WikiPage.objects.get(url=url)
                    page.content = content
                    page.last_editor = request.user
                    page.edited_datetime = timezone.now()
                    page.save()

                    return redirect('wiki-page', url=url)
                else:
                    return render(request, 'wiki/edit.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': form, 'wiki_page': WikiPage.objects.get(url=url)})
            else:
                return render(request, 'wiki/edit.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': PageChangeForm(initial={'content': WikiPage.objects.get(url=url).content}), 'wiki_page': WikiPage.objects.get(url=url)})
        else:
            return render(request, 'layout/message.html', {
                'message_type': "error",
                'message_title': "Wiki page does not exist!",
                'message_content': "Wiki page with that URL does not exist!"
            })
    else:
        return render(request, 'layout/message.html', {
            'message_type': "error",
            'message_title': "Not logged in!",
            'message_content': "You need to be logged in in order to do that."
        })


def page_delete(request, url):
    if request.user.is_authenticated:
        if not request.user.has_perm('wiki.delete_wikipage'):
            return render(request, 'layout/message.html', {
                'message_type': "error",
                'message_title': "Insufficient permissions.",
                'message_content': "You don't have the permission to do that!"
            })
        if WikiPage.objects.filter(url=url).exists():
            if request.method == 'POST':
                form = PageDeleteForm(request.POST)
                if form.is_valid():

                    page = WikiPage.objects.get(url=url)
                    page.delete()

                    return redirect('wiki-index')
                else:
                    return render(request, 'wiki/delete.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': form, 'wiki_page': WikiPage.objects.get(url=url)})
            else:
                return render(request, 'wiki/delete.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': PageDeleteForm(), 'wiki_page': WikiPage.objects.get(url=url)})
        else:
            return render(request, 'layout/message.html', {
                'message_type': "error",
                'message_title': "Wiki page does not exist!",
                'message_content': "Wiki page with that URL does not exist!"
            })
    else:
        return render(request, 'layout/message.html', {
            'message_type': "error",
            'message_title': "Not logged in!",
            'message_content': "You need to be logged in in order to do that."
        })
