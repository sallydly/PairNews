from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):

	# return HttpResponse("Hello world!!")
	context = {}
	return render(request,template_name="gotnews_app/base.html", context=context)

def _expand_row(request):
	return HttpResponse("This will return the data to expand a row with.")
