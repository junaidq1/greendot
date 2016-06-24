from django.contrib import admin

# Register your models here.

from .models import Review, Employee, Vote

class ReviewModelAdmin(admin.ModelAdmin):
	list_display = ["pk", "__unicode__", 'employee', 'user', 'timestamp', 'upvotes', 'downvotes']
	list_display_links = ["__unicode__", 'employee', 'timestamp']
	list_filter = ['timestamp']
	#list_editable
	search_fields = ['content']
	class Meta:
		model = Review

class EmployeeModelAdmin(admin.ModelAdmin):
	list_display = ['pk', 'full_name', 'first_name', 'last_name', 'level', 'office', 'timestamp']
	list_display_links = ['first_name', 'last_name', 'level', 'office', 'timestamp']
	list_filter = ['first_name', 'last_name', 'level', 'office', 'timestamp']
	#list_editable
	search_fields = ['first_name', 'last_name', 'level', 'office', 'timestamp']
	
	class Meta:
		model = Employee

class VoteModelAdmin(admin.ModelAdmin):
	list_display = ['pk','user', 'review', 'employee', 'upvotes', 'downvotes']
	list_display_links = ['user', 'review', 'employee','upvotes', 'downvotes']
	list_filter = ['review', 'employee', 'user', 'upvotes']
	#list_editable
	search_fields = ['review', 'employee', 'user', 'upvotes']
	
	class Meta:
		model = Vote	

admin.site.register(Review, ReviewModelAdmin) #, Employee) #, Employee) #, EmployeeModelAdmin)
admin.site.register(Employee, EmployeeModelAdmin)
admin.site.register(Vote, VoteModelAdmin)