from django.shortcuts import render
from .models import WikiPage


def index(request):
    return page(request, 'wiki-index')


def page(request, url):
    passed = dict()

    wiki_page = WikiPage.objects.get(url=url)
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

    return render(request, 'wiki/page.html', passed)
