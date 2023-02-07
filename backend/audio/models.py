from django.db import models

class AudioClip(models.Model):
    file = models.FileField(upload_to='clips')
    