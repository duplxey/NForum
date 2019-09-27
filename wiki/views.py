from django.shortcuts import render


def index(request):
    return render(request, 'wiki/index.html', {})


def page(request):
    return render(request, 'wiki/page.html', {})