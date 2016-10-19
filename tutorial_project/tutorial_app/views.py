from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse('Here will be tutorial')
def index(request):
	context_dict = {'boldmessage':'tutorials here'}
	return HttpResponse("Here will be tutorial")
def index(request):
	context_dict={'boldmessage':'tutorials here!'}
	return render(request, 'index.html', context_dict)
