from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from directory.models import User, Technology, Project, Cohort
from django.utils.translation import gettext_lazy as _


class DirectoryUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'avatar',)}),
        (_('Momentum info'), {"fields": (
            "cohort", "is_momentum_staff", "looking_for_job", "specialities", "interests",
        )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class CohortAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'slug',
    )
    prepopulated_fields = {"slug": ('name',)}


admin.site.register(User, DirectoryUserAdmin)
admin.site.register(Technology)
admin.site.register(Project)
admin.site.register(Cohort, CohortAdmin)
