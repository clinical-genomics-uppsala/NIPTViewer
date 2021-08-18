from dataprocessor.utils.data import import_data_into_database
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def load(request):
    import_data_into_database("test.csv")
    return HttpResponse(status=200)
