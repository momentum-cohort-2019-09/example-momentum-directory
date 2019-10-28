from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from directory.models import User, Technology, Project, Cohort

admin.site.register(User, UserAdmin)
admin.site.register(Technology)
admin.site.register(Project)
admin.site.register(Cohort)
