from django.contrib import admin
from oddasat.translations.models import Translation

def resave(modeladmin, request, queryset):
	for item in queryset:
		item.save()

resave.short_description = 'Re-save all items'	

class TransAdmin(admin.ModelAdmin):
	model = Translation
	list_display = ('id','last_translated', 'translated_title', 'last_hash')
	list_editable = ('last_hash',)
	actions = [resave]


admin.site.register(Translation, TransAdmin)
