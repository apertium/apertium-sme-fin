from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
from settings import here

urlpatterns = patterns('',
	(r'^m/(?P<path>.*)$', 'django.views.static.serve', {'document_root': here('m')}),
    # Example:
	(r'^translations/', include('translations.urls')),
	(r'^feeds/', include('feeds.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
)
