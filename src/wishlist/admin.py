from django.contrib import admin
from django import forms
# Register your models here.
 
from .models import Wishlist, Fvote

class WishlistAdmin(admin.ModelAdmin):
	list_display = ["pk", "__unicode__",'feature','user', 'f_timestamp']
	list_display_links = ["__unicode__",'feature','user', 'f_timestamp']
	list_filter = ['f_timestamp', 'user', 'feature']
	#list_editable
	search_fields = ['user', 'feature']
	
	class Meta:
		model = Wishlist

class FvoteAdmin(admin.ModelAdmin):
	list_display = ["pk", 'feature','user', 'feature_votes', 'fv_timestamp']
	list_display_links = ['feature','user', 'feature_votes', 'fv_timestamp']
	list_filter = ['fv_timestamp', 'user', 'feature']
	#list_editable
	search_fields = ['user', 'feature']
	
	class Meta:
		model = Fvote


admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Fvote, FvoteAdmin)