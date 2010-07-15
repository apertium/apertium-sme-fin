# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.conf import settings

from feeds.models import Feed, Article

def article_detail(request, tid):
	context = {}
	template = 'feeds/translation_detail.html'
	T = get_object_or_404(Article, id=tid)
	
	context['article'] = T
	return render_to_response(template, context, context_instance=RequestContext(request))

def feed_detail(request, fid):
	context = {}
	template = 'feeds/feed_detail.html'
	T = get_object_or_404(Article, id=tid)

	context['article'] = T
	return render_to_response(template, context, context_instance=RequestContext(request))


def feeds_list(request):
	context = {}
	template = 'feeds/feeds_list.html'
	
	Fs = Feed.objects.all()
	context['feeds'] = Fs
	
	return render_to_response(template, context, context_instance=RequestContext(request))


def article_list(request):
	context = {}
	template = 'articles/articles_list.html'
	
	Ts = Article.objects.order_by('pub_date')
	context['articles'] = Ts
	
	return render_to_response(template, context, context_instance=RequestContext(request))
