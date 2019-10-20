from django.shortcuts import render


def not_authenticated(request):
    return render(request, 'layout/message.html', {
        'message_type': "error",
        'message_title': "Not logged in.",
        'message_content': "You need to be logged in in order to do that."
    })


def insufficient_permission(request):
    return render(request, 'layout/message.html', {
        'message_type': "error",
        'message_title': "Insufficient permissions.",
        'message_content': "You don't have the permission to do that!"
    })


def unknown_wiki_page(request):
    return render(request, 'layout/message.html', {
        'message_type': "error",
        'message_title': "Wiki page does not exist!",
        'message_content': "Wiki page with that URL does not exist!"
    })