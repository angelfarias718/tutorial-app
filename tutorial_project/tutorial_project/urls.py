from django.conf.urls import patterns, include, url
from django.contrib import admin
<<<<<<< HEAD
from django.conf.urls.static import static
from django.conf import settings

=======
from django.conf import settings
from django.conf.urls.static import static
>>>>>>> 459f27552dc1899c1423957cf32db4e7fe731399

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tutorial_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
<<<<<<< HEAD
	url(r'^', include('tutorial_app.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
	url(r'^', include('tutorial_app.urls')), # ADD THIS NEW TUPLE!
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 459f27552dc1899c1423957cf32db4e7fe731399
