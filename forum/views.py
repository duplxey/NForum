from django.shortcuts import render

from .models import *


def index_view(request):
    return render(request, 'forum/index.html', {'categories': Category.objects.all()})


def thread_view(request):
    return render(request, 'forum/thread.html', {})


def subcategory_view(request):
    return render(request, 'forum/subcategory.html', {})
