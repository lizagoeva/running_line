from django.http import HttpRequest
from django.shortcuts import render


def create_video(request: HttpRequest):
    context = {

    }
    return render(request, 'create_video/index-page.html', context=context)
