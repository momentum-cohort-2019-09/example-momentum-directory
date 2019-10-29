from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


def index_view(request):
    user = request.user
    return render(request, "directory/index.html")


@login_required
def accounts_profile(request):
    return render(request, 'directory/profile.html')
