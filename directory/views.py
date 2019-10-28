from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index_view(request):
    user = request.user
    return render(request, "directory/index.html", {"user": user})
