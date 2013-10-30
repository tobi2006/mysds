from django.db import models
from django.contrib.auth.models import User
from database.models import Student

class student_teacher_appointment(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    student = models.ForeignKey(Student, blank=True, null=True)
    teacher = models.ForeignKey(User)

# Make sure to delete these appointments at the end of the year - no need to keep all this garbage!
