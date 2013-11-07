from django.db import models
from django.contrib.auth.models import User
from database.models import Student

class AppointmentBlock(models.Model):
    teacher = models.ForeignKey(User)
    message = models.TextField(blank=True, null=True)
    invited = models.ManyToManyField(Student, blank=True, null=True, related_name="invited")

class StudentTeacherAppointment(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    student = models.ForeignKey(Student, blank=True, null=True)
    belongs_to = models.ForeignKey(AppointmentBlock, related_name="appointment")




# Make sure to delete these appointments at the end of the year - no need to keep all this garbage!
