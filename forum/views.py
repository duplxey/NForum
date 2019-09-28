from django.shortcuts import render

from .models import *


def index(request):
    return render(request, 'forum/index.html', {'categories': Category.objects.all()})


def thread(request):
    return render(request, 'forum/thread.html', {})


def subcategory(request):
    return render(request, 'forum/subcategory.html', {})
