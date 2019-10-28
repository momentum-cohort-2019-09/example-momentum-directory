from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_momentum_staff = models.BooleanField(default=False)
    cohort = models.ForeignKey(to='Cohort',
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True,
                               related_name='members')
    specialities = models.ManyToManyField(to='Technology',
                                          blank=True,
                                          related_name='specialists')
    interests = models.ManyToManyField(to='Technology',
                                       blank=True,
                                       related_name='enthusiasts')


class Technology(models.Model):
    name = models.CharField(max_length=255)


class Cohort(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(to=User,
                                     related_name='projects',
                                     blank=True)
    technologies = models.ManyToManyField(to=Technology,
                                          related_name='projects',
                                          blank=True)
    video_url = models.URLField(blank=True, null=True)
    repo_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True)
    final_project_for_cohort = models.ForeignKey(to=Cohort,
                                                 on_delete=models.SET_NULL,
                                                 related_name='final_projects',
                                                 null=True,
                                                 blank=True)
