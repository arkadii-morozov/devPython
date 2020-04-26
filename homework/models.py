from django.db import models

class Students(models.Model):
    name = models.CharField(max_length=32, null=False)
    surname = models.CharField(max_length=32, null=False)
    full_name = models.CharField(max_length=65, null=False)

    def __str__(self):
        return f'{self.surname} {self.name}'

    def __repr__(self):
        return f'Student(name="{self.name}", surname="{self.surname}"'

class Subjects(models.Model):
   name = models.CharField(max_length=32, null=False)

class Score(models.Model):
   full_name = models.CharField(max_length=65, null=False)
   subject = models.CharField(max_length=32, null=False)
   bal = models.FloatField()