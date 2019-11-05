from django.db import models
from django.db.models import Q, F
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse


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
    looking_for_job = models.BooleanField(
        "Are you currently looking for a job?", default=True)
    avatar = models.ImageField(upload_to='user_avatars/', null=True)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("person_detail", kwargs={"username": self.username})

    def autogenerate_username(self):
        """
        Use the first and last name to generate a username. If the username
        is a duplicate, add a incrementing number to the end.
        """
        counter = 0
        while not self.username:
            username_candidate = f"{self.first_name.lower()[0]}{self.last_name.lower()}"
            if counter > 0:
                username_candidate += str(counter)
            if User.objects.filter(username=username_candidate).count() > 0:
                counter += 1
            else:
                self.username = username_candidate

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
    end_date = models.DateField()

    class Meta:
        ordering = ['-end_date']
        constraints = [
            models.CheckConstraint(name='start_date_lte_end_date',
                                   check=Q(start_date__lte=F('end_date')))
        ]

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

    def get_absolute_url(self):
        return reverse("cohort_detail", kwargs={"slug": self.slug})

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
    screenshot = models.ImageField(upload_to='project_screenshots/', null=True)
