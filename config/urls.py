"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from directory import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
    path('accounts/profile/', views.accounts_profile, name='profile'),
    path('projects/', views.project_list, name='project_list'),
    path('cohorts/<slug:slug>/', views.cohort_detail, name='cohort_detail'),
    path('cohorts/<slug:slug>/edit_projects/',
         views.cohort_edit_final_projects,
         name="cohort_edit_final_projects"),
    path('cohorts/<slug:slug>/add_student/',
         views.cohort_add_student,
         name="cohort_add_student"),
    path('people/<slug:username>/', views.person_detail, name='person_detail'),
    path('', views.index_view, name='index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
