from django.shortcuts import render
from .models import WikiPage


def index(request):
    return page(request, 'wiki-index')


def page(request, url):
    passed = dict()

    wiki_page = WikiPage.objects.get(url=url)
    passed['wiki_page'] = wiki_page

    try:
        next_wiki_page = WikiPage.objects.get(pk=wiki_page.pk + 1)
        passed['next_wiki_page'] = next_wiki_page
    except WikiPage.DoesNotExist:
        passed['next_wiki_page'] = None

    try:
        previous_wiki_page = WikiPage.objects.get(pk=wiki_page.pk - 1)
        passed['previous_wiki_page'] = previous_wiki_page
    except WikiPage.DoesNotExist:
        passed['previous_wiki_page'] = None

    return render(request, 'wiki/page.html', passed)
