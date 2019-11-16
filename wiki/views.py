from django.shortcuts import redirect
from django.utils import timezone

from nforum.errors import *
from wiki.forms import PageAddForm, PageChangeForm, PageDeleteForm
from .models import WikiPage


def index_view(request):
    return page_view(request, 'wiki-index')


def page_view(request, url):
    passed = dict()

    try:
        wiki_page = WikiPage.objects.get(url=url)
    except WikiPage.DoesNotExist:
        return unknown_wiki_page(request)

    passed['wiki_page'] = wiki_page
    passed['next_wiki_page'] = wiki_page.get_next_page
    passed['previous_wiki_page'] = wiki_page.get_previous_page
    passed['wiki_pages'] = WikiPage.objects.all()

    if request.user.is_authenticated:
        permissions = {
            'add': request.user.has_perm('wiki.add_wikipage'),
            'change': request.user.has_perm('wiki.change_wikipage'),
            'delete': request.user.has_perm('wiki.delete_wikipage'),
        }
        passed['user_permissions'] = permissions

    return render(request, 'wiki/view.html', passed)


def page_add(request):
    if not request.user.is_authenticated:
        return not_authenticated(request)

    if not request.user.has_perm('wiki.add_wikipage'):
        return insufficient_permission(request)

    if request.method == 'POST':
        form = PageAddForm(request.POST)

        if not form.is_valid():
            return render(request, 'wiki/add.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': form})

        display_index = form.cleaned_data['display_index']
        title = form.cleaned_data['title']
        url = form.cleaned_data['url'].lower()
        content = form.cleaned_data['content']

        page = WikiPage.objects.create(display_index=display_index, title=title, url=url, content=content, author=request.user)
        page.save()

        return redirect('wiki-page', url=url)
    else:
        return render(request, 'wiki/add.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': PageAddForm()})


def page_change(request, url):
    if not request.user.is_authenticated:
        return not_authenticated(request)

    if not request.user.has_perm('wiki.change_wikipage'):
        return insufficient_permission(request)

    if not WikiPage.objects.filter(url=url).exists():
        return unknown_wiki_page(request)

    if request.method == 'POST':
        form = PageChangeForm(request.POST)

        if not form.is_valid():
            return render(request, 'wiki/change.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': form, 'wiki_page': WikiPage.objects.get(url=url)})

        content = form.cleaned_data['content']

        page = WikiPage.objects.get(url=url)
        page.content = content
        page.last_editor = request.user
        page.edited_datetime = timezone.now()
        page.save()

        return redirect('wiki-page', url=url)
    else:
        return render(request, 'wiki/change.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': PageChangeForm(initial={'content': WikiPage.objects.get(url=url).content}), 'wiki_page': WikiPage.objects.get(url=url)})


def page_delete(request, url):
    if not request.user.is_authenticated:
        return not_authenticated(request)

    if not request.user.has_perm('wiki.delete_wikipage'):
        return insufficient_permission(request)

    if not WikiPage.objects.filter(url=url).exists():
        return unknown_wiki_page(request)

    if request.method == 'POST':
        form = PageDeleteForm(request.POST)

        if not form.is_valid():
            return render(request, 'wiki/delete.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': form, 'wiki_page': WikiPage.objects.get(url=url)})

        page = WikiPage.objects.get(url=url)
        page.delete()

        return redirect('wiki-index')
    else:
        return render(request, 'wiki/delete.html', {'wiki_pages': WikiPage.objects.all().order_by('display_index'), 'form': PageDeleteForm(), 'wiki_page': WikiPage.objects.get(url=url)})
