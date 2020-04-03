from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def index_view(request):
    # If the user is authenticated, he probably doesn't want to see that presentation page
    if request.user.is_authenticated:
        return redirect('forum-home')

    return render(request, 'home/index.html', {'user_count': User.objects.all().count()})
