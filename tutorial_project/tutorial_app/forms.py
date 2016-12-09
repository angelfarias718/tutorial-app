from django import forms
from models import Page, Category, UserProfile
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password', 'email')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website', 'picture', 'bio')

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter a category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Category
		fields = ('name',)
		exclude = ('user',)


class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
	url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		if url and not url.startswith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url
			
		return cleaned_data

	class Meta:
		model = Page
		exclude = ('category', 'user')


class ContactForm(forms.Form):
	name = forms.CharField(required=True)
	email = forms.CharField(widget=forms.EmailInput(), required=True)
	subject = forms.CharField(required=True)
	body = forms.CharField(widget=forms.Textarea(), required=True)	

	def send_message(self):
		name = self.cleaned_data['name']
		email = self.cleaned_data['email']
		subject = self.cleaned_data['subject']
		body = self.cleaned_data['body']

		message = '''
				New Message from {name} @ {email}
				Subject: {subject}
				Message:
				{body}
				'''.format(name=name,
					email=email,
					subject=subject,
					body=body)

		email_msg = EmailMessage('New Contact Form Submission',
					message,
					email,
					['angelcodewriter@gmail.com'])

		email_msg.send()


class PasswordRecoveryForm(forms.Form):
		email = forms.EmailField(required=False)

		def clean_email(self):
				try:
						return User.objects.get(email=self.cleaned_data['email'])
				except User.DoesNotExist:
						raise forms.ValidationError("Can't find user based on the email")
				return self.cleaned_data['email']

		def reset_email(self):
			user = self.cleaned_data['email']

			password = get_random_string(length=8)
			user.set_password(password)
			user.save()

			body = """
					Sorry you are having issues with your Prosecutor DB account.  Below is your username and new password:
				
					Username: {username}
					Password: {password}
				
					You can login here: http://localhost:8000/login/
					Change your password here: http://localhost/settings/

					""".format(username=user.username, password=password)

			pw_msg = EmailMessage('Your new Password', body, 'angelcodewriter@gmail.com', [user.email])
					
			pw_msg.send()


