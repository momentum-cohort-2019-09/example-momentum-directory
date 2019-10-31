from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from directory.forms import ProfileForm
from directory.models import Cohort, User, Project
from django.db.models import Q
from django.views.generic.detail import DetailView

# Create your views here.


def index_view(request):
    return render(request, "directory/index.html")


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


class PersonDetailView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'directory/person_detail.html'

    def get_queryset(self):
        return User.objects.filter(cohort__isnull=False)


# same as:
# def person_detail(request, username):
#     user = get_object_or_404(User, username=username)
#     return render(request, 'directory/person_detail.html', {"user": user})
