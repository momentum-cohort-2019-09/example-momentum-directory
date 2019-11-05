import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.db.models import Q
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.template.loader import render_to_string
from django.urls import reverse

from directory.forms import NewStudentForm, ProfileForm
from directory.models import Cohort, Project, User

momentum_staff_required = user_passes_test(
    lambda u: u.is_authenticated and u.is_momentum_staff)


def index_view(request):
    latest_cohort = Cohort.objects.filter(
        end_date__lte=timezone.now().date()).order_by('-end_date')[0]
    return render(request, "directory/index.html", {"cohort": latest_cohort})


@login_required
def accounts_profile(request):
    if request.method == "POST":
        form = ProfileForm(instance=request.user,
                           data=request.POST,
                           files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(to='profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'directory/profile.html', {"form": form})


def cohort_detail(request, slug):
    cohort = get_object_or_404(Cohort, slug=slug)
    members = cohort.members.order_by("last_name")
    return render(request, 'directory/cohort_detail.html', {
        "cohort": cohort,
        "members": members,
    })


@login_required
@momentum_staff_required
def cohort_edit_final_projects(request, slug):
    cohort = get_object_or_404(Cohort, slug=slug)
    ProjectFormSet = inlineformset_factory(Cohort,
                                           Project,
                                           fields=(
                                               'name',
                                               'description',
                                               'repo_url',
                                               'video_url',
                                               'demo_url',
                                               'screenshot',
                                           ))

    if request.method == "POST":
        formset = ProjectFormSet(data=request.POST,
                                 files=request.FILES,
                                 instance=cohort)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    else:
        formset = ProjectFormSet(instance=cohort)
    return render(request, 'directory/cohort_edit_final_projects.html', {
        "cohort": cohort,
        'formset': formset
    })


@login_required
@momentum_staff_required
def cohort_add_student(request, slug):
    cohort = get_object_or_404(Cohort, slug=slug)

    if request.method == "POST":
        form = NewStudentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.cohort = cohort
            student.autogenerate_username()
            student.password = uuid.uuid4()
            student.save()

            send_mail(
                'A new user account was created for you at Momentum Directory',
                render_to_string(
                    'directory/new_student_email.txt', {
                        "student": student,
                        "password_reset_url": request.build_absolute_uri(
                            reverse('auth_password_reset'))
                    }),
                settings.DEFAULT_FROM_EMAIL,
                [student.email],
            )

            return redirect(to='cohort_detail', slug=cohort.slug)

    form = NewStudentForm()
    return render(request, 'directory/cohort_add_student.html', {
        "cohort": cohort,
        "form": form
    })


def project_list(request):
    projects = Project.objects.all()
    search_term = request.GET.get('search')
    if search_term:
        projects = projects.filter(
            Q(description__icontains=search_term) |
            Q(name__icontains=search_term) |
            Q(technologies__name__icontains=search_term))

    return render(request, "directory/project_list.html",
                  {"projects": projects})


def person_detail(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'directory/person_detail.html', {"user": user})
