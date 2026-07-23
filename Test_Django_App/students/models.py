from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course, related_name='students', blank=True,)

    def __str__(self):
        return self.name

