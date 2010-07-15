# encoding: utf-8
from django.db import models
import datetime
import hashlib
from apertium.apertium import apertium # heh
import re
# from oddasat.feeds import Article

# from oddasat.feedjack.models import Post

# from feedjack.models import Post #  as Article
# Article.objects.filter(link__contains='iltalehti')
# .save()

# class Article(Post, models.Model):
# 	class Meta:
# 		proxy = True
# 	
# 	def __init__(self, *args, **kwargs):
# 		super(Post, self).__init__(*args, **kwargs)
# 		self.cleaned_body = self.content
# 
# 	def save(self, *args, **kwargs):
# 		super(Post, self).save(*args, **kwargs)
# 		self.cleaned_body = self.content
# 		print "*** Translating article %s" % repr(self)
# 		translate, created = Translation.objects.get_or_create(article=self)
# 		if not created:
# 			print "*** Retranslating article?"
# 			translate.save()
# 
# 		print "*** Article saved."
	



# from django.conf import settings
# 
# if settings.CELERY:
# 	from celery.decorators import task
# 	apertium_wrap = task(apertium, task_is_eager=False)
# else:
# 	apertium_wrap = apertium

# def apertium_wrap(*args, **kwargs):
# 	print args
# 	text = apertium(*args, **kwargs)
# 	return text

TEST = """Tämä on joku testauslause. Minä näin kaksi koiraa."""

# >>> from oddasat.feeds.models import Feed, FeedItem
# >>> new = Feed.objects.create()
# >>> item = new.feeditem_set.all()[0]
# >>> tx = Translation.objects.create(article=item)
# >>> tx.save()
# >>> print tx.translated_text
# >>> a = apertium_wrap.delay('Minä näin kaksi koiraa', debug=True, cache=False)

asdf = re.compile(r'(?P<begchunk>\{)?(\^[^\$\W\w\<\>]+\$(?:\s)?)+')
punct = re.compile(r'\^punct<CLB>\{\^.<CLB>\$\}\$')

def align_analysis(sen, chu):
	"""
		Takes a sentence and a chunked version of the sentence, and returns a list of dictionaries...
	"""
	print "aligning"
	sen_ = sen.split(' ')
	chu_ = chu.split(' ')
	
	def find_end(windex, chunks):
		cut = chunks[windex::]
		out_chunk = []
		
		for part in cut:
			end = True and part.find('$}$') > -1 or False
			out_chunk.append((cut.index(part)+windex, part))
			if end:
				break
		
		return out_chunk
	
	def consume(point, count, L):
		for wipe_index in range(count+1)[1::]:
			L[wipe_index] = '-'
	
	
	aligned = []
	backtrack = 0
	for word in sen_:
		windex = sen_.index(word)
		subchunk = chu_[windex]
		subchunk_nop = punct.sub('', chu_[windex])
		start = True and subchunk_nop.find('{') > -1 or False
		end = True and subchunk_nop.endswith('$}$') or False
		
		# If the word fits in one chunk, then append it
		
		if end and start:
			align = (word, subchunk, False, False) 
			backtrack = 0
		elif start and not end:
			# Otherwise if it begins a chunk, find the end (getting the whole chunk)
			# And append (word, subchunk, other_words, whole_chunk)
			c_ = find_end(windex, chu_)
			other_words = [sen_[ind] for ind, thing in c_]
			whole_chunk = ' '.join([a[1] for a in c_])
			align = (word, subchunk, other_words, whole_chunk)
			# backtrack is the index that we'll be copying from later 
			backtrack = -1
		elif not start:
			align = (word, subchunk, aligned[backtrack + windex][2], aligned[backtrack + windex][3])
			backtrack -= 1 
		aligned.append(align)
	
	keys = ['lemma', 'chunk', 'other_lemmas', 'whole_chunk']
	aligned = [dict(zip(keys,a)) for a in aligned]	
	return aligned


class Translation(models.Model):
	""" Translation item, generic relation later...  
		
		>>> a = apertium('Minä näin kaksi koiraa', debug=True, cache=False, opts='-f html')
		>>> a.wait()
		'Mun oidnen guokte beatnaga'
		>>> from oddasat.feeds.models import Feed, FeedItem
		>>> new = Feed.objects.create()
				
		
	"""
	article = models.ForeignKey('feeds.Article')
	input_text = models.TextField(blank=True)
	translated_title = models.CharField(max_length=320, blank=True)
	translated_text = models.TextField(blank=True)
	last_hash = models.CharField(max_length=320)
	chunked = models.TextField(blank=True)
	tagged = models.TextField(blank=True)
	last_translated = models.DateTimeField(default=datetime.datetime.now())
	
	def chunked_format_split(self):
		sentences_aligned = None
		if self.translated_text and self.chunked:
			tx = self.translated_text
			ch = self.chunked
			ch_ = ch.splitlines()
			tx_ = tx.splitlines()
			lines = zip(tx_, ch_)
			sentences_aligned = []
			for sen, chu in lines:
				aligned = align_analysis(sen, chu)
				sentences_aligned.append(aligned)
		return sentences_aligned
	
	def chunked_format(self):
		# TODO: span wrapping for highlighting chunks
		return self.chunked
	
	def __unicode__(self):
		try:
			return u"<Translation for: %s>" % self.article.title
		except:
			return u"<Translation for: unknown>"
	
	def save(self, *args, **kwargs):
		# Here's where I do the translation, but first check that the last_hash hasn't changed (e.g., article has been fetched again)
		# only get the full text, but option for chunk and etc.
		
		if kwargs.has_key('just_save'):
			del kwargs['just_save']
			super(Translation, self).save(*args, **kwargs)
		else:
			self.translate(self)
			super(Translation, self).save(*args, **kwargs)
	
	def __init__(self, *args, **kwargs):
		super(Translation, self).__init__(*args, **kwargs)
		# try:
		# 	self.original_text = self.article.cleaned_body
		# except Exception, e:
		# try:
		# 	self.original_text = self.article.content
		# except:
		# 	pass
		# 
		# try:
		# 	self.article_title = self.article.title
		# except:
		# 	pass
		# try:
		# 	self.article_pub_date = self.article.pub_date
		# except:
		# 	pass
		#try:
		#	self.article_title = self.article.title
		#	self.article_pub_date = self.article.pub_date
		#	self.article_url = self.article.url
		#except:
		#	pass
		
	def highlight_unknown(self):
		"""
			Wraps unknown words in spans for highlighting by css
		"""
		t = self.translated_text
		word_match = re.compile(r'(?P<m>\@|\#|\*)(?P<w>\w+)', re.U)
		t = word_match.sub('<span class="unknownwd"><span>\g<m></span>\g<w></span>', t)
		return t
	
	def hide_symbols(self):
		# TODO: hide @ and # and *, etc.
		pass
	
	def chunk(self):
		if self.article:
			if self.article.cleaned_body:
				in_text = self.article.cleaned_body
			else:
				in_text = self.article.data
			if self.article.title:
				in_title = self.article.title
			else:
				in_title = 'Ei otsikkoa'
		elif self.input_text:
			in_text = self.input_text
		self.chunked = apertium(in_text, cache=False, subcommand='chunker')
		self.save(just_save=True)
		return True
	
	# def translate(new_hash, chunk=False, tag=False):
	def translate(self, chunk=False, tag=False):
		# self.translated_text = apertium(self.article.data, cache=False)
		if self.article:
			if self.article.cleaned_body:
				in_text = self.article.cleaned_body
			else:
				in_text = self.article.data
			if self.article.title:
				in_title = self.article.title
			else:
				in_title = 'Ei otsikkoa'
		elif self.input_text:
			in_text = self.input_text
		
		# self.last_hash = hashlib.sha1(str(in_text)).hexdigest()
		# 
		# if self.last_hash != hashlib.sha1(str(in_text)).hexdigest():
		print "--> Sending to apertium"
		self.translated_title = apertium(in_title, cache=False)
		if self.article.item_type == 'html':
			opts = '-f html'
		else:
			opts = ''
		
		self.translated_text = apertium(in_text, cache=False, opts=opts) #, opts='-f html')
		self.last_translated = datetime.datetime.now()
		if chunk:
			self.chunked = apertium(in_text, cache=False, subcommand='chunker')
		
		self.last_hash = '1234'
		
		return True
		
	