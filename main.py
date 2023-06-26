import os
from math import ceil
import cv2
import numpy as np

SIZE = (100, 100)
VIDEO_DURATION = 3  # in seconds
TEXT_STRING = 'Бегущая строка'
FONT = cv2.FONT_HERSHEY_COMPLEX
SCALE, THICKNESS = 3, 3
TEXT_COLOR = (255, 255, 255)  # white


def name_videofile(filename='running_line.mp4'):
    """
    Generates name for a video file
    Gives unique name with number, if several videos were generated

    :param filename: prefered filename, by default 'running_line.mp4'
    :return: Resulting filename for saving
    """
    if os.path.exists(filename):
        name = filename.split('.')[0]
        file_num = 1
        while True:
            filename = f'{name}{file_num}.mp4'
            if not os.path.exists(filename):
                break
            file_num += 1
    return filename


def generate_video(text, duration):
    """
    Creates video with running line and saves it
    :param text: String you want to put into the running line
    :param duration: Approximate duration of video (in seconds)
    :return: None
    """
    video_name = name_videofile()
    if text:
        text_size = cv2.getTextSize(text, FONT, SCALE, THICKNESS)[0]  # text size in pixels
    else:
        print('Строка не может быть пустой')
        return

    fps = 60
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_name, fourcc, fps, SIZE)

    x = SIZE[0]
    x_shift = ceil((SIZE[0] + text_size[0]) / fps / duration)
    while x > -text_size[0]:
        img = np.zeros((SIZE[1], SIZE[0]), dtype=np.uint8)
        cv2.putText(img, text, (x, 80), FONT, SCALE, TEXT_COLOR, THICKNESS)
        cv2.imwrite('background.jpg', img)
        img = cv2.imread('background.jpg')
        out.write(img)
        x -= x_shift

    cv2.destroyAllWindows()
    out.release()
    print(f'Видео сохранено под именем файла {video_name}')
    try:
        os.remove('background.jpg')
    except FileNotFoundError:
        pass


generate_video(text=TEXT_STRING, duration=VIDEO_DURATION)
