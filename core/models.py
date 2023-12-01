from django.db import models

class Anime(models.Model):
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    genre = models.CharField(max_length=100)
    trailer_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title