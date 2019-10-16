from django.shortcuts import render
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

    return render(request, 'wiki/page.html', passed)
