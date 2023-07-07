from math import ceil
import cv2
import os
import numpy as np
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import VideoRequests


def index_page(request: HttpRequest):
    context = {}
    return render(request, 'create_video/index-page.html', context=context)


def video_making_func(text, duration):
    font = cv2.FONT_HERSHEY_COMPLEX
    scale, thickness, size, color = 3, 3, (100, 100), (255, 255, 255)
    video_name = 'running_line.mp4'
    if text:
        text_size = cv2.getTextSize(text, font, scale, thickness)[0]  # text size in pixels
    else:
        print('Строка не может быть пустой')
        return

    fps = 60
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_name, fourcc, fps, size)

    x = size[0]
    x_shift = ceil((size[0] + text_size[0]) / fps / duration)
    while x > -text_size[0]:
        img = np.zeros((size[1], size[0]), dtype=np.uint8)
        cv2.putText(img, text, (x, 80), font, scale, color, thickness)
        cv2.imwrite('background.jpg', img)
        img = cv2.imread('background.jpg')
        out.write(img)
        x -= x_shift
    cv2.destroyAllWindows()
    out.release()
    try:
        os.remove('background.jpg')
    except FileNotFoundError:
        pass
    return video_name


def downloader(filename):
    response = HttpResponse(open(filename, "rb"), content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def create_video(request: HttpRequest):
    text_was_changed, duration_was_changed = True, True
    text = request.GET.get('text')
    duration = request.GET.get('time')
    if not text:  # setting default values
        text = 'glad to see you'
        text_was_changed = False
    if not duration or not duration.isdigit():
        duration = 3
        duration_was_changed = False
    duration = int(duration)
    filename = video_making_func(text=text, duration=duration)
    context = {
        'text': text,
        'duration': duration,
        'filename': filename,
        'filepath': os.path.abspath(filename),
    }
    VideoRequests.objects.create(
        text_in_video=text,
        custom_text=text_was_changed,
        video_duration=duration,
        custom_duration=duration_was_changed,
        video_filename=filename,
    )
    return downloader(filename)
    # return render(request, 'create_video/create-video.html', context=context)


def show_database(request: HttpRequest):
    context = {
        'video_creation_requests': VideoRequests.objects.all(),
    }
    return render(request, 'create_video/show-database.html', context=context)
