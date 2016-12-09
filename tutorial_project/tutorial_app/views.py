from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from models import Category, Page, UserProfile
from forms import CategoryForm, PageForm, UserForm, UserProfileForm, ContactForm, PasswordRecoveryForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash 
from django.contrib.auth.decorators import login_required
from datetime import datetime
from search import run_query
from suggest import get_category_list
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from braces.views import LoginRequiredMixin


def index (request):
	context_dict = {}

	#request.session.set_test_cookie()
	#if request.session.test_cookie_worked():
	#	print ">>>>TEST COOKIE WORKED!"
	#	request.session.delete_test_cookie()

	
	category_list = Category.objects.order_by('-likes')[:5]

	context_dict['categories'] = category_list
	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages'] = page_list

	visits = request.session.get('visits')

	if not visits:
		visits = 1



	reset_last_visit_time = False

	#if 'last_visit' in request.COOKIES:
	#	last_visit = request.COOKIES['last_visit']
	last_visit = request.session.get('last_visit')
	if last_visit: #if the cookie exists
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

		if (datetime.now() - last_visit_time).days > 0:
			visits = visits + 1
			reset_last_visit_time = True

	else:
		reset_last_visit_time = True

	context_dict['visits'] = visits
		
	

	if reset_last_visit_time:
		#response.set_cookie('last_visit', datetime.now())
		#response.set_cookie('visits', visits)
		request.session['last_visit'] = str(datetime.now())

		
	context_dict['visits'] = visits
	response = render(request, 'index.html', context_dict)
	return response

def about (request):

	context_dict = {}

	if request.session.get('visits'):
		count = request.session.get('visits')
	else: count = 0

	count = count + 1
	context_dict['visits'] = count


	return render(request, 'about.html', context_dict)

def category(request, category_name_slug):
	context_dict = {}
	context_dict['results_list'] = None
	context_dict['query'] = None

	if request.method == 'POST':
			query = request.POST['query'].strip()

			if query:
				result_list = run_query(query)

				context_dict['result_list'] = result_list
				context_dict['query'] = query

	try:
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		pages = Page.objects.filter(category=category).order_by('-views')
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass

	if not context_dict['query']:
		context_dict['query'] = category.name


	return render(request, 'category.html', context_dict)



@login_required
def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			cat = form.save(commit=False)
			cat.user = request.user
			cat.save()

			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()

	return render(request, 'add_category.html', {'form':form})


@login_required
def add_page(request, category_name_slug):
		try:

				cat = Category.objects.get(slug=category_name_slug)
		except Category.DoesNotExist:
				cat = None

		if request.method == 'POST':
				form = PageForm(request.POST)

				if form.is_valid():
						if cat:
								page = form.save(commit=False)
								page.user = request.user
								page.category = cat
								page.views = 0
								page.save()
								return category(request, category_name_slug)
						else:
								print form.errors
				else:
						print form.errors
		else:
				form = PageForm()

		context_dict = {'form':form, 'category':cat, 'slug':category_name_slug}
		return render(request, 'add_page.html', context_dict)


def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profle_form.save(commit=false)

			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			register = True

		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'register.html', { 'user_form': user_form, 'profile_form': profile_form, 'registered': registered }
	)


def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse("Your account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'login.html', {})

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def track_url(request):
	page_id = None

	url = '/'

	if request.method == 'GET':
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']
			try:
				page = Page.objects.get(id=page_id)
				page.views = page.views + 1
				page.save()
				url = page.url
			except:
				pass
	return redirect(url)


def user_profile(request, user_username):
	context_dict = {}
	user = User.objects.get(username=user_username)
	profile = UserProfile.objects.get(user=user)
	context_dict['profile'] = profile
	context_dict['pages'] = Page.objects.filter(user=user)

	return render(request, 'profile.html', context_dict)

def edit_profile(request, user_username):
	profile = get_object_or_404(UserProfile, user__username=user_username)
	website = profile.website
	pic = profile.picture
	bio = profile.bio
	if request.user != profile.user:
		return	HttpResponse('Access Denied')

	if request.method == 'POST':
		form = UserProfileForm(data=request.POST)
		if form.is_valid():

			if request.POST['website'] and request.POST['website'] != '':
				profile.website = request.POST['website']
			else:
				profile.website = website

			if request.POST['bio'] and request.POST['bio'] != '':
				profile.bio = request.POST['bio']
			else:
				profile.bio = bio

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']	
			else:
				profile.picture = pic

			profile.save()

			return user_profile(request, profile.user.username)
		else:
			print form.errors
	else:
		form = UserProfileForm()
	return render(request,
					'edit_profile.html',
					{'form':form, 'profile':profile})


def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)

		if form.is_valid():
			form.send_message()
			return HttpResponseRedirect('/')
		else:
			print form.errors
	else:
		form = ContactForm()

	return render(request, 'contact.html', {'form':form})

@login_required
def like_category(request):
		cat_id = None
		if request.method == "GET":
				cat_id = request.GET['category_id']

		likes = 0

		if cat_id:
				cat = Category.objects.get(id=int(cat_id))
				if cat:
						likes = cat.likes + 1
						cat.likes = likes
						cat.save()
		return HttpResponse(likes)

def suggest_category(request):
	cat_list = []
	starts_with = ''

	if request.method == 'GET':
		starts_with = request.GET['suggestion']

	cat_list = get_category_list(8, starts_with)

	print cat_list

	return render(request, 'cat.html', {'cats': cat_list })

@login_required
def auto_add_page(request):
	cat_id = None
	url = None
	title = None
	user = None
	context_dict = {}

	if request.method == 'GET':
		cat_id = request.GET['category_id']
		url = request.GET['url']
		title = request.GET['title']
		user = request.GET['user']

		if cat_id and user:
			category = Category.objects.get(id=int(cat_id))
			user = User.objects.get(username=user)
			p = Page.objects.get_or_create(category=category, user=user, title=title, url=url)

			pages = Page.objects.filter(category=category).order_by('-views')			

			context_dict['pages'] = pages

	return render(request, 'page_list.html', context_dict)



class SettingsView(LoginRequiredMixin, FormView):
	template_name = 'settings.html'
	form_class = PasswordChangeForm
	success_url = reverse_lazy('index')
	login_url = '/login/'
	def get_form(self, form_class):
		return form_class(user=self.request.user, **self.get_form_kwargs())

	def form_valid(self, form):
		form.save()
		update_session_auth_hash(self.request, form.user)
		return super(SettingsView, self).form_valid(form)


class PasswordRecoveryView(FormView):
	template_name = 'password_recovery.html'
	form_class = PasswordRecoveryForm
	success_url = reverse_lazy('login')
	def form_valid(self, form):
		form.reset_email()
		return super(PasswordRecoveryView, self).form_valid(form)



