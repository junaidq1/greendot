from django.contrib import admin

# Register your models here.

from .models import Review, Employee, Vote, UserStatus

class ReviewModelAdmin(admin.ModelAdmin):
	list_display = ["pk", "__unicode__",'work_again','employee', 'user', 'timestamp']
	list_display_links = ["__unicode__", 'employee', 'timestamp']
	list_filter = ['timestamp', 'user', 'employee']
	#list_editable
	search_fields = ['content']
	class Meta:
		model = Review

class EmployeeModelAdmin(admin.ModelAdmin):
	list_display = ['pk', 'full_name', 'first_name', 'last_name', 'level', 'office', 'service_area', 'timestamp']
	list_display_links = ['first_name', 'last_name', 'level', 'office','service_area', 'timestamp']
	list_filter = ['first_name', 'last_name', 'level', 'office', 'service_area','timestamp']
	#list_editable
	search_fields = ['first_name', 'last_name', 'level', 'office','service_area', 'timestamp']
	
	class Meta:
		model = Employee

class VoteModelAdmin(admin.ModelAdmin):
	list_display = ['pk','user', 'review', 'employee', 'upvotes', 'downvotes', 'v_timestamp']
	list_display_links = ['user', 'review', 'employee','upvotes', 'downvotes','v_timestamp']
	list_filter = ['review', 'employee', 'user', 'upvotes']
	#list_editable
	search_fields = ['review', 'employee', 'user', 'upvotes']
	
	class Meta:
		model = Vote	

class UserStatusAdmin(admin.ModelAdmin):
	list_display = ['pk','user', 'is_contributor', 'updated']
	list_display_links = ['pk','user', 'is_contributor', 'updated']

	search_fields = ['pk','user', 'is_contributor', 'updated']
	class Meta:
		model = UserStatus


admin.site.register(Review, ReviewModelAdmin) #, Employee) #, Employee) #, EmployeeModelAdmin)
admin.site.register(Employee, EmployeeModelAdmin)
admin.site.register(Vote, VoteModelAdmin)
admin.site.register(UserStatus, UserStatusAdmin)