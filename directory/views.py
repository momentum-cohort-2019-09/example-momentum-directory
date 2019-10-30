from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from directory.forms import ProfileForm
from directory.models import Cohort

# Create your views here.


def index_view(request):
    return render(request, "directory/index.html")


@login_required
def accounts_profile(request):
    if request.method == "POST":
        form = ProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'directory/profile.html', {"form": form})


def cohort_detail(request, pk):
    cohort = get_object_or_404(Cohort, pk=pk)
    return render(request, 'directory/cohort_detail.html', {"cohort": cohort})
