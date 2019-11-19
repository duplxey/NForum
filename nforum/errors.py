from django.shortcuts import render


def not_authenticated(request):
    return render(request, 'layout/message.html', {
        'message_type': "error",
        'message_title': "Not logged in.",
        'message_content': "You need to be logged in in order to do that."
    })


def already_authenticated(request):
    return render(request, 'layout/message.html', {
        'message_type': "error",
        'message_title': "You are already logged in.",
        'message_content': "You are already logged in, are you trying to break something? o.O"
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


def unknown_user(request):
    return render(request, 'layout/message.html', {
        'message_type': "error",
        'message_title': "Unknown user!",
        'message_content': "This user does not exist."
    })


def unknown_subcategory(request):
    return render(request, 'layout/message.html', {
        'message_type': "error",
        'message_title': "Unknown subcategory!",
        'message_content': "Could not find the requested subcategory."
    })


def unknown_thread(request):
    return render(request, 'layout/message.html', {
        'message_type': "error",
        'message_title': "Unknown thread!",
        'message_content': "Could not find the requested thread."
    })


def unknown_message(request):
    return render(request, 'layout/message.html', {
        'message_type': "error",
        'message_title': "Unknown message!",
        'message_content': "Could not find the requested message."
    })


def search_failed(request):
    return render(request, 'layout/message.html', {
        'message_type': "error",
        'message_title': "Search failed!",
        'message_content': "Search could fail due to the following reasons:"
                           "<ul>"
                           "<li>No query was specified.</li>"
                          "<li>Query was shorter than 2 characters.</li>"
                          "<li>Query was longer than 16 characters.</li>"
                           "</ul>"
    })
