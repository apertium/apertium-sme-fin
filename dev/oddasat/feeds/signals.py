from oddasat.data.rss_parse import fetchURL

# from oddasat.feeds.models import FeedItem ; a = FeedItem.objects.all() ; a[0].save()
from celery.decorators import task
import time

from django.conf import settings

if settings.CELERY:
	fetchURL = task(fetchURL).delay
else:
	pass
	
def fetch_feeditem(item):
	"""
		Fetches data for feed item.
	"""

	# do stuff
	# print "Signal called."
	data = fetchURL(item.url)	

	try:
		while not data.ready():
			# print "waiting: %s" % str(data.ready())
			continue
		else:
			if data.ready():
				data = data.result
	except:
		pass

	return data


def fetch_feeditem_sig(sender, **kwargs):
	"""
		Fetches data for feed item.
	"""
	feeditem = kwargs['instance']
	
	data = fetch_feeditem(feeditem)
	
	feeditem.data = data
	return True
