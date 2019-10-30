from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


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
    looking_for_job = models.BooleanField(default=True)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Cohort(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True)
    start_date = models.DateField()

    def save(self, *args, **kwargs):
        counter = 0
        while not self.slug:
            possible_slug = slugify(self.name)
            if counter > 0:
                possible_slug = possible_slug + "-" + counter
            collisions = Cohort.objects.filter(slug=possible_slug)
            if collisions.count() == 0:
                self.slug = possible_slug
            else:
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


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
