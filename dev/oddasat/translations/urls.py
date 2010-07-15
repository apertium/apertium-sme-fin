# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns


urlpatterns = patterns('translations.views',
	(r'^(?P<tid>\d+)/re_save/$', 're_save'),
	(r'^(?P<tid>\d+)/chunk/$', 'do_translation_chunk'),
	(r'^(?P<tid>\d+)/$', 'translation_detail'),
	(r'^$', 'translations_list'),
)