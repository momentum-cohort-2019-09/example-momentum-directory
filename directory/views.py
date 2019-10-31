from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
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


@login_required
@require_POST
@csrf_exempt
def toggle_project_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project in request.user.favorites.all():
        request.user.favorites.remove(project)
    else:
        request.user.favorites.add(project)
    return JsonResponse({"ok": True})


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
