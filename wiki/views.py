from django.contrib.auth.decorators import login_required
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


@login_required
def page_add(request):
    if not request.user.has_perm('wiki.add_wikipage'):
        return insufficient_permission(request)

    form = PageAddForm()

    if request.method == 'POST':
        form = PageAddForm(data=request.POST)

        if form.is_valid():
            display_index = form.cleaned_data['display_index']
            title = form.cleaned_data['title']
            url = form.cleaned_data['url'].lower()
            content = form.cleaned_data['content']

            wiki_page = WikiPage.objects.create(display_index=display_index, title=title, url=url, content=content, author=request.user)
            wiki_page.save()

            return redirect('wiki-page', url=url)

    return render(request, 'wiki/add.html', {
        'wiki_pages': WikiPage.objects.all(),
        'form': form,
    })


@login_required
def page_change(request, url):
    if not request.user.has_perm('wiki.change_wikipage'):
        return insufficient_permission(request)

    try:
        wiki_page = WikiPage.objects.get(url=url)
    except WikiPage.DoesNotExist:
        return unknown_wiki_page(request)

    form = PageChangeForm(instance=wiki_page)

    if request.method == 'POST':
        form = PageChangeForm(instance=wiki_page, data=request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']

            wiki_page.content = content
            wiki_page.last_editor = request.user
            wiki_page.edited_datetime = timezone.now()
            wiki_page.save()

            return redirect('wiki-page', url=url)

    return render(request, 'wiki/change.html', {
        'wiki_pages': WikiPage.objects.all(),
        'form': form,
        'wiki_page': wiki_page,
    })


@login_required
def page_delete(request, url):
    if not request.user.has_perm('wiki.delete_wikipage'):
        return insufficient_permission(request)

    try:
        wiki_page = WikiPage.objects.get(url=url)
    except WikiPage.DoesNotExist:
        return unknown_wiki_page(request)

    form = PageDeleteForm()

    if request.method == 'POST':
        form = PageDeleteForm(data=request.POST)

        if form.is_valid():
            wiki_page.delete()

            return redirect('wiki-index')

    return render(request, 'wiki/delete.html', {
        'wiki_pages': WikiPage.objects.all(),
        'form': form,
        'wiki_page': wiki_page,
    })
