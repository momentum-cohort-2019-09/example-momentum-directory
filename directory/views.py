from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from directory.forms import ProfileForm
from directory.models import Cohort, User
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


class PersonDetailView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'directory/person_detail.html'
