from django.db import models

# Create your models here.
class Episode(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.CharField(max_length=255)
    guid = models.CharField(max_length=255)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return f"{self.podcast_name}: {self.title}"
