from django.shortcuts import render
from django.http import HttpResponse

<<<<<<< HEAD
def index (request):
	context_dict = {'boldmessage':'tutorials here!'}


	return render(request, 'index.html', context_dict)

def about (request):
	return HttpResponse ('About Us')
=======
def index(request):
    return HttpResponse('Here will be tutorial')
def index(request):
	context_dict = {'boldmessage':'tutorials here'}
	return HttpResponse("Here will be tutorial")
def index(request):
	context_dict={'boldmessage':'tutorials here!'}
	return render(request, 'index.html', context_dict)
>>>>>>> 459f27552dc1899c1423957cf32db4e7fe731399
