from django.db import models

class MapStyle(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title
