# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns


urlpatterns = patterns('feeds.views',
	(r'^$', 'feeds_list'),
)

urlpatterns += patterns('translations.views',
	(r'^(?P<feedid>\d+)/(?P<txt>txt)/', 'translations_list'),
	(r'^(?P<feedid>\d+)/', 'translations_list'),
)