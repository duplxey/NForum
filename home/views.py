from django.contrib.auth.models import User
from django.shortcuts import render


def index_view(request):
    return render(request, 'home/index.html', {'user_count': User.objects.all().count()})
