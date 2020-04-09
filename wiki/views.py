from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone

from nforum.errors import *
from wiki.forms import PageAddForm, PageChangeForm, PageDeleteForm
from .models import WikiPage

landing_wiki_text = \
    "<p style='text-align: center; font-weight:600;'>Welcome to NForum.</p>" \
    "<p style='text-align: center;'>NForum is a simple light-weight forum written in Python using Django. It allows users to create their own threads or talk in already existing ones. It has a built-in upvote/downvote (reputation) system, achievements, alerts & more!</p>" \
    "<p style='text-align: center;'><img src='https://i.imgur.com/JVuVPFA.gif' alt='' width='300' height='169'/></p>" \
    "<p style='text-align: center;'>The project is completely open-sourced on GitHub:</p>" \
    "<p style='text-align: center;'><a href='https://github.com/duplxey/NForum'>https://github.com/duplxey/NForum</a></p>"


def index_view(request):
    # If there are no pages yet, let's create a landing one
    if WikiPage.objects.count() == 0:
        WikiPage.objects.create(display_index=1, title="Wiki Index", url="index", content=landing_wiki_text)

    return page_view(request, WikiPage.objects.first().url)


def page_view(request, url):
    try:
        wiki_page = WikiPage.objects.get(url=url)
    except WikiPage.DoesNotExist:
        return unknown_wiki_page(request)

    return render(request, 'wiki/view.html', {
        'wiki_page': wiki_page,
        'next_wiki_page': wiki_page.get_next_page,
        'previous_wiki_page': wiki_page.get_previous_page,
        'wiki_pages': WikiPage.objects.all()
    })


@login_required
def page_add(request):
    if not request.user.has_perm('wiki.add_wikipage'):
        return insufficient_permission(request)

    form = PageAddForm(initial={'display_index': WikiPage.get_first_empty()})

    if request.method == 'POST':
        form = PageAddForm(data=request.POST, initial={'display_index': WikiPage.get_first_empty()})

        if form.is_valid():
            display_index = form.cleaned_data['display_index']
            title = form.cleaned_data['title']
            url = form.cleaned_data['url'].lower()
            content = form.cleaned_data['content']

            wiki_page = WikiPage.objects.create(display_index=display_index, title=title, url=url, content=content, author=request.user)
            wiki_page.save()

            return redirect('wiki-page', url=url)

    return render(request, 'wiki/form/add.html', {
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

    return render(request, 'wiki/form/change.html', {
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

    return render(request, 'wiki/form/delete.html', {
        'wiki_pages': WikiPage.objects.all(),
        'form': form,
        'wiki_page': wiki_page,
    })
