from directory.models import Cohort


def add_cohorts(request):
    return {"cohorts": Cohort.objects.order_by("start_date")}
