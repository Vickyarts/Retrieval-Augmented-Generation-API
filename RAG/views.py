from django.shortcuts import render


def interface(request):
    return render(request, 'chat.html')