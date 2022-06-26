from django.db import models
from django.utils import timezone



class Reader(models.Model):
    file = models.FileField(blank=True, null=True)
    date_uploaded = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_uploaded']
        verbose_name_plural = "Reader"