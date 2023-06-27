from django.db import models


class VideoRequests(models.Model):
    text_in_video = models.TextField(null=False, blank=False)
    custom_text = models.BooleanField()
    video_duration = models.PositiveIntegerField(null=False, blank=False)
    custom_duration = models.BooleanField()
    creation_time = models.DateTimeField(auto_now_add=True)
    video_filename = models.TextField(null=False, blank=False)
