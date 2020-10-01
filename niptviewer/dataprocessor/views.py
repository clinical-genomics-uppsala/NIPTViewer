from django.shortcuts import render
from django.http import HttpResponse
from dataprocessor.utils.data import import_data_into_database
# Create your views here.
def load(request):
    try:
        import_data_into_database("test.csv")
    except:
        #return  HttpResponse(status=500)
        pass
    return  HttpResponse(status=200)
