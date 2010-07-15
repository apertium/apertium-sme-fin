from django.contrib import admin
from oddasat.feeds.models import Feed, Article

# from feedjack.admin import *

def set_no_fetch(modeladmin, request, queryset):
	for item in queryset:
		item.no_refetch = True
		item.save()

set_no_fetch.short_description = 'Set all items to not fetch.'

class FeedAdmin(admin.ModelAdmin):
	list_display = ('name', 'url')
	pass

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'pub_date', 'feed', 'disable_item', 'no_refetch')
	list_editable = ('disable_item', 'no_refetch')
	actions = [set_no_fetch]
	model = Article
	extra = 3

admin.site.register(Feed, FeedAdmin)
admin.site.register(Article, ArticleAdmin)
