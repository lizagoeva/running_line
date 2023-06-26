from math import ceil
import cv2
import os
import numpy as np
from django.http import HttpRequest
from django.shortcuts import render


def index_page(request: HttpRequest):
    context = {}
    return render(request, 'create_video/index-page.html', context=context)


def video_making_func(text, duration):
    print(f'duration = {duration}')
    font = cv2.FONT_HERSHEY_COMPLEX
    scale, thickness, size, color = 3, 3, (100, 100), (255, 255, 255)
    video_name = 'running_line.mp4'
    if text:
        text_size = cv2.getTextSize(text, font, scale, thickness)[0]  # text size in pixels
        print(f'text_size = {text_size}')
    else:
        print('Строка не может быть пустой')
        return

    fps = 60
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_name, fourcc, fps, size)

    x = size[0]
    x_shift = ceil((size[0] + text_size[0]) / fps / duration)
    print(f'x_shift = {x_shift}')
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


def create_video(request: HttpRequest):
    text = request.GET.get("text")
    duration = request.GET.get("time")
    if not text:  # setting default values
        text = 'glad to see you'
    if not duration or not duration.isdigit():
        duration = 3
    duration = int(duration)
    filename = video_making_func(text=text, duration=duration)
    context = {
        'text': text,
        'duration': duration,
        'filename': filename,
        'filepath': os.path.abspath(filename),
    }
    return render(request, 'create_video/create-video.html', context=context)
