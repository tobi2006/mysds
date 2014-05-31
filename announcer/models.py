from django.db import models
from django.contrib.auth.models import User


class Announcement(models.Model):
    ANNOUNCE_TO = (
        ('students', 'Students'),
        ('teachers', 'Staff'),
        ('all', 'All')
        )

    author = models.ForeignKey(User)
    publishing_date = models.DateTimeField()
    text = models.TextField(blank=True, null=True)
    headline = models.CharField(max_length=200, blank=True, null=True)
    announce_to = models.CharField(max_length=20, choices=ANNOUNCE_TO)

    class Meta:
        ordering = ['-publishing_date', 'author']
