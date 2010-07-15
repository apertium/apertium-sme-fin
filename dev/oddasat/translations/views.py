# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.conf import settings

from translations.models import Translation

def re_save(request, tid):
	# TODO: post only
	T = get_object_or_404(Translation, id=tid)
	T.save()
		
	return HttpResponseRedirect('/articles/%s/' % tid)


def do_translation_chunk(request, tid):
	# TODO: post only
	T = get_object_or_404(Translation, id=tid)
	T.chunk()
	
	
	return HttpResponseRedirect('/articles/%s/' % tid)

def translation_detail(request, tid):
	context = {}
	template = 'translations/translation_detail.html'
	T = get_object_or_404(Translation, id=tid)
	
	context['article'] = T
	return render_to_response(template, context, context_instance=RequestContext(request))


def translations_list(request, feedid=None, txt=None):
	context = {}
	if txt:
		template = 'translations/plaintext.txt'
	else:
		template = 'translations/translations_list.html'
	if feedid:
		Ts = Translation.objects.filter(article__feed__id=feedid)
		context['feed'] = Ts[0].article.feed
	else:
		Ts = Translation.objects.order_by('-article__pub_date')
	context['articles'] = Ts
	
	return render_to_response(template, context, context_instance=RequestContext(request))
