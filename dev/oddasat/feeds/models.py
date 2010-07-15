from django.db import models
import datetime
import re

# import feedparser

# 
from data.rss_parse import Article, parseRSS, fetchURL
from oddasat.translations.models import Translation
# 
from django.utils.html import strip_tags, linebreaks

# 
from feeds.signals import fetch_feeditem
# 
# # 
# # class Post(Post):
# # 	class Meta:
# # 		proxy = True
# # 	
# # 	def save(self, *args, **kwargs):
# # 		super(Post, self).save(*args, **kwargs)
# # 		
# # 		print "*** Translating article %s" % repr(self)
# # 		translate, created = Translation.objects.get_or_create(article=self)
# # 		if not created:
# # 			print "*** Retranslating article?"
# # 			translate.save()
# # 			
# # 		print "*** Article saved."
# # 
# # 
# 
# 
# # Create your models here.
# _DEBUG = True
# from feedjack.models import Feed
# 
class Feed(models.Model):
	"""
		Feed: rss only for now
		
		>>> new_feed = Feed.objects.create(url="feed://www.hs.fi/uutiset/rss/")
		>>> new_feed.save()
	"""
	
	name = models.CharField(max_length=80)
	# feed = models.ForeignKey(Feed)
	url = models.URLField(default='http://www.iltalehti.fi/rss/rss.xml')
	article_type = models.CharField(max_length=10, help_text='filetype for parsing guidance')
	
	content_tag = models.CharField(max_length=80, blank=True)
	
	clip_text = models.BooleanField(default=True, help_text='If true, use clip_start and clip_end, otherwise content_pattern')
	clip_start = models.CharField(max_length=80, default='<!-- lapset -->', help_text='Begin clip text here.')
	clip_end = models.CharField(max_length=80, default='<div class="clear"></div>', help_text='End clip here.')
	
	class Admin:
		pass
	
	def __unicode__(self):
		return '<Feed at %s>' % self.url
	
	def save(self, *args, **kwargs):
		super(Feed, self).save(*args, **kwargs)
		self.url = self.url.replace('feed','http')
		articles = parseRSS(self.url)
		
		for post in articles:
			print ''
			try:
				exists = self.article_set.get(feed=self, url=post.link)
				print "*** Article existed already: %s" % repr(exists)
				exists.pub_date = post.pub_date
				exists.item_type   = self.article_type
				exists.title       = post.title
				exists.clip_start  = self.clip_start
				exists.clip_end    = self.clip_end
				exists.content_tag = self.content_tag
				exists.save()
				print "*** Resaving with new metadata from Feed."
			except Article.DoesNotExist:
				new = self.article_set.create(
					feed=self, 
					# post=post,
					url=post.link, 
					pub_date=post.pub_date, 
					item_type=self.article_type,
					title=post.title,
					clip_start=self.clip_start,
					clip_end=self.clip_end,
					content_tag=self.content_tag,
				)				
				print "*** Creating new article: %s" % repr(new)
		return True
 	
linebreak = re.compile(r'\n+|(\n\t)')
carriage = re.compile(r'\r')
fix_linebreaks = lambda x: linebreak.sub('\n', carriage.sub('', x))
# 
# from feedjack.models import Post
# 
class Article(models.Model):
	"""Items belonging to feed"""
	
	feed = models.ForeignKey(Feed)
	# post = models.ForeignKey(Post)
	disable_item = models.BooleanField(default=False, help_text="Disable fetching and hide item in translations.")
	title = models.CharField(max_length=120)
	url = models.URLField(blank=True, verify_exists=False)
	
	no_refetch = models.BooleanField(default=False, help_text='Check this to disable fetching and clipping when the item is saved.')
	item_type = models.CharField(max_length=12, default="html", help_text="Article document type.")
	
	content_tag = models.CharField(max_length=80, blank=True, help_text="Regex match for article content")
	
	clip_text = models.BooleanField(default=True)
	clip_start = models.CharField(max_length=80, default='<p class="articleParagraph">', help_text='Begin clip text here.')
	clip_end = models.CharField(max_length=80, default='<script type="text/javascript">', help_text='End clip here.')
	
	fetched_last = models.DateTimeField(default=datetime.datetime.now())
	pub_date = models.DateTimeField(blank=True)
	data = models.TextField(blank=True)
	cleaned_body = models.TextField(blank=True)
	
	class Admin:
		pass
	
	def clip_text(self):
		if self.clip_start:
			trunc1 = self.clip_start
			text = trunc1 + self.data.partition(trunc1)[2]
		if self.clip_end:
			trunc2 = self.clip_end
			text = text.partition(trunc2)[0].strip()
		
		# self.cleaned_body = fix_linebreaks(strip_tags(text)).strip()
		self.cleaned_body = text
	
	def save(self, *args, **kwargs):
		# Fetch article and save data; html2text? html2text can apparently fetch URLs, maybe that saves trouble.
		if self.disable_item:
			self.no_refetch = True
			self.data = 'None'
			self.cleaned_body = 'None'
			super(Article, self).save(*args, **kwargs)
			return False
		
		if not self.no_refetch:
			data = fetch_feeditem(self)
			self.data = data
		
		if self.clip_text:
			self.clip_text()
			print "*** Cleaned body text"
		
		super(Article, self).save(*args, **kwargs)
		print "*** Translating article %s" % repr(self)
		translate, created = Translation.objects.get_or_create(article=self)
		if not created:
			print "*** Retranslating article?"
			translate.save()
			
		print "*** Article saved."
	
	def get_absolute_url(self):
		return '/%s/%d/%d' % ('feeds', self.feed.id, self.id)
	
	def __str__(self):
		return '<Article: %s - %s>' % (self.feed.name, self.url) 



# from django.dispatch import Signal
# item_saved = Signal(providing_args=["omg", "bbq"])
# 
# # signal registration
# from django.db.models.signals import post_save, pre_save
# from oddasat.feeds.signals import fetch_feeditem_sig
# 
# # pre_save.connect(fetch_feeditem, sender=Article, dispatch_uid="oddasat.feeds.models.post_save")
# pre_save.connect(fetch_feeditem_sig, sender=Feed, dispatch_uid="oddasat.feeds.models.post_save")
