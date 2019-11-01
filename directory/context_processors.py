from directory.models import Cohort
from django.utils import timezone


def add_cohorts(request):
    cohorts = Cohort.objects.order_by("start_date")
    if not (request.user.is_authenticated and request.user.is_momentum_staff):
        cohorts = cohorts.filter(end_date__lte=timezone.now().date())
    return {"cohorts": cohorts}
