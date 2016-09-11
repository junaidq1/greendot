from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Review, Employee, Vote, VoteManager, UserLevel
from .forms import ReviewForm2, ValidationForm, ContactForm, AccessIssuesForm, ReportDataForm, UserLevelRegistrationForm, PartnerForm
from django.db.models import Q
from django.contrib.auth.models import User #test this guy - remove if needed
from django.db.models import Count, Sum, Avg
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib import messages
from registration.backends.default.views import RegistrationView
import csv
# Create your views here.


 
# def import_db(request):
# 	#csv_filepathname=
# 	dataReader = csv.reader(open('/home/greendot/webapps/greendotpeers/employees2.csv'), delimiter=',', quotechar='"')
# 	for row in dataReader:
# 		emp = Employee()
# 		emp.first_name = row[0]
# 		emp.last_name = row[1]
# 		emp.email = row[2]
# 		emp.level = row[3]
# 		emp.service_area = row[4]
# 		emp.service_line = row[5]
# 		emp.office = row[6]
# 		emp.save()
# 	return HttpResponse("Completed", content_type="text/plain")



def go_home(request):	
	return render(request, "home.html", {})

def about(request):
	return render(request, "about.html", {})

def faqs(request):
	return render(request, "faqs.html", {})

@login_required
def review_list(request):
	queryset = Review.objects.all()

	if request.user.is_superuser:
		context = {"obj_list": queryset}
	else:
		context = {"title": "Unauthenticated List"}
	return render(request, "review_list.html", context)  #render takes in request, a template and a context


def verify_question(request):
	# data = request.POST.get('my_form_field_name')	
	form = ValidationForm(request.POST or None)
	message =''
	if form.is_valid():
		a = form.cleaned_data.get("answer") #request.POST['answer']
		if (a == 'impact day') or (a == 'Impact Day') or (a == 'Impact day') :
			return HttpResponseRedirect('/accounts/register/')
		else:
			message = "Incorrect Answer"
	context = {
	'form': form,
	'val_message': message,
	}
	return render(request, "create_username_prestep.html", context)

# def review_create(request):
# 	form = ReviewForm(request.POST or None)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.save()
# 		return HttpResponseRedirect(instance.get_absolute_url())
# 		#form.cleaned_data.get("content")
# 	# if request.method == "POST":
# 	# 	cont = request.POST.get("content")
# 	# 	emp = request.POST.get("employee")
# 		#Review.objects.create(content=cont, employee=Employee.objects.get(pk=emp))

	# context = {
	# 	"form": form,
	# }
	# return render(request, "post_form.html", context)

@login_required
def review_create1(request):
	queryset_list = Employee.objects.filter(is_live=True)
	query = request.GET.get("q1")
	if query:  #add an or here
		queryset_list = queryset_list.filter(
						Q(last_name__icontains=query)
						)
		#print queryset_list
	context = {
	"queryset_list":queryset_list,
	"query": query
	}
	return render(request, "create_review1.html", context)
		#return HttpResponseRedirect('/reviews/create2/')

@login_required
def review_create2(request, pk=None):
	#form = ReviewForm(request.POST or None)
	#instance = get_object_or_404(Review, pk=pk) #this is what was working_1
	#form = ReviewForm(request.POST or None, instance=instance) #this is what was working_2	
	obj = Employee.objects.get(pk=pk)
	form = ReviewForm2(request.POST or None)
	if form.is_valid():
		try:
			instance = form.save(commit=False)
			instance.employee = Employee.objects.get(pk=pk)
			instance.user = request.user
			instance.save()
			return HttpResponseRedirect('/reviews/create3/')
		except:
			return HttpResponseRedirect('/reviews/error/')
	context = {
		"form": form,
		"obj": obj,
	}
	return render(request, "create_review2.html", context)


def rev_error(request):
	return render(request, "cant_review_twice.html", {})

@login_required
def review_create3(request):
	return render(request, "create_review3.html", {})


@login_required
def review_detail(request, pk=None):
	instance = get_object_or_404(Review, pk=pk)
	context = {
		"instance": instance
	}
	return render(request, "detail.html", context)


# def review_update(request, pk=None):
# 	instance = get_object_or_404(Review, pk=pk)
# 	form = ReviewForm(request.POST or None, instance=instance)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.save()
# 		return HttpResponseRedirect(instance.get_absolute_url())
# 	context = {
# 		"instance": instance,
# 		"form": form,
# 	}
# 	return render(request, "post_form.html", context)


def review_delete(request):
	return HttpResponse("<h1>delete</h1>")

@login_required
def employee_list(request):
	queryset = Employee.objects.all()

	if request.user.is_superuser:
		context = {"obj_list": queryset}
	else:
		context = {"title": "Unauthenticated List"}
	return render(request, "employee_list.html", context) 

@login_required
def employee_detail(request, pk=None):
	instance = get_object_or_404(Employee, pk=pk)
	rev_list = instance.review_set.all() #.order_by("-count('upvotes')")
	rev_list = rev_list.annotate(num_votes=Count('votereview')).order_by('-num_votes')
	rev_count = instance.review_set.count()
	ques1_overall_avg = Review.objects.aggregate(Avg('ques1'))
	ques1_overall_avg = ques1_overall_avg['ques1__avg']
	ques2_overall_avg = Review.objects.aggregate(Avg('ques2'))
	ques2_overall_avg = ques2_overall_avg['ques2__avg']
	ques3_overall_avg = Review.objects.aggregate(Avg('ques3'))
	ques3_overall_avg = ques3_overall_avg['ques3__avg']
	ques1_employee_avg = rev_list.aggregate(Avg('ques1'))
	ques1_employee_avg = ques1_employee_avg['ques1__avg']
	ques2_employee_avg = rev_list.aggregate(Avg('ques2'))
	ques2_employee_avg = ques2_employee_avg['ques2__avg']
	ques3_employee_avg = rev_list.aggregate(Avg('ques3'))
	ques3_employee_avg = ques3_employee_avg['ques3__avg']
	work_again_yes = rev_list.filter(work_again__iexact="Y").aggregate(Count('work_again'))	
	work_again_yes =work_again_yes['work_again__count']
	work_again_no = rev_list.filter(work_again__iexact="N").aggregate(Count('work_again'))	
	work_again_no =work_again_no['work_again__count']
	#vote_list = instance.vote_set.all()
	context = {
		"review_list": rev_list,
		"rev_count": rev_count,
		"instance": instance,
		"ques1_overall_avg": ques1_overall_avg,
		"ques2_overall_avg": ques2_overall_avg,
		"ques3_overall_avg": ques3_overall_avg,
		"ques1_employee_avg": ques1_employee_avg,
		"ques2_employee_avg": ques2_employee_avg,
		"ques3_employee_avg": ques3_employee_avg,
		"work_again_yes": work_again_yes,
		"work_again_no": work_again_no,
		#"rand_num": rand_num,
	}
	#print rand_num
	return render(request, "employee_detail.html", context)


@login_required
def vote_for_review(request, pk=None, pk2=None):
	emp_instance = get_object_or_404(Employee, pk=pk)
	rev_instance = get_object_or_404(Review, pk=pk2)
	#print emp_instance
	#print rev_instance
	vote_status = "unsuccessfully"
	if request.user.is_authenticated():
		try:
			us = request.user
			Vote.objects.create(user = us, review=rev_instance, employee= emp_instance, upvotes=True) 
			#content=cont, employee=Employee.objects.get(pk=emp))
			vote_status = "successfully"
		except:
			return HttpResponseRedirect('/reviews/vote_error/')
	context = {
		"vote_status": vote_status
	}		
	return render(request, "voted.html", context)	


def vote_error(request):
	return render(request, "cant_vote_twice.html", {})

#this function basically controls what the user homepage looks like 
# based on users authentication status and contributor status
def goto_userpage(request):
	if request.user.is_authenticated() and request.user.userstatus.is_contributor:
		#Pull in the 5 most recent reviews to show folks on the homepage
		recent_reviews = Review.objects.filter(employee__is_live=True).order_by('-pk')[:5]
		#Pull in the 5 most recently likes reviews on the homepage
		recent_voted_reviews = Vote.objects.filter(employee__is_live=True).order_by('-pk')[:5]
		## count the number of reviews by user
		rev_count = request.user.review_set.count()
		## pull in all votes for each review and count them
		user_review_queryset = Review.objects.filter(user=request.user).order_by('-timestamp')
		user_review_queryset = user_review_queryset.annotate(num_votes=Count('votereview'))
		vote_ct = 0
		for obj in user_review_queryset:
				vote_ct = vote_ct + obj.num_votes
		
		context = {
		"username": request.user,  #update this
		"recent_reviews": recent_reviews,
		"recent_voted_reviews": recent_voted_reviews,
		"review_count": rev_count,
		#"vote_count": vote_count,
		#"user_review_queryset": user_review_queryset, #not needed for now, can add later
		"vote_ct": vote_ct,
		} 
		return render(request, "user_homepage.html", context)
	else:
		if request.user.is_authenticated() and request.user.userstatus.is_contributor == False:
			return render(request, "become_a_contributor.html", {}) 
		else:
			return render(request, "home.html", {})  

@login_required
def search_practitioner_reviews(request):
	#queryset_list = Employee.objects.all()   #add active filter here
	queryset_list = Employee.objects.filter(is_live=True)
	query = request.GET.get("q1")
	if query:  #add an or here
		queryset_list = queryset_list.filter(
						Q(last_name__icontains=query)
						)
		#print queryset_list
	context = {
	"queryset_list":queryset_list,
	"query": query
	}
	return render(request, "search_practitioners1.html", context)
		#return HttpResponseRedirect('/reviews/create2/')

@login_required
def view_past_user_reviews(request, pk=None):
	user_review_queryset = Review.objects.filter(user=request.user).order_by('-timestamp')
	#review_votes = user_review_queryset.annotate(num_votes=Count('votereview'))
	user_review_queryset = user_review_queryset.annotate(num_votes=Count('votereview'))
	
	context = {
	"username": request.user,  
	"user_review_queryset": user_review_queryset,
	#"review_votes": review_votes,
	}
	return render(request, "all_reviews_by_user.html", context)


#new - long list of practitioners recently reviewed
@login_required
def list_of_reviewed_employees(request):
	if request.user.is_authenticated() and request.user.userstatus.is_contributor:
		recent_reviews1 = Review.objects.filter(employee__is_live=True).order_by('-pk')[:25]
		recent_reviews2 = Review.objects.filter(employee__is_live=True).order_by('-pk')[25:50]
		#update recent_voted_reviews after model refresh
		context = {
		"username": request.user,  #update this
		"recent_reviews1": recent_reviews1,
		"recent_reviews2": recent_reviews2,
		} 
		return render(request, "recent_reviews_longlist.html", context)
	else:
		if request.user.is_authenticated() and request.user.userstatus.is_contributor == False:
			return render(request, "become_a_contributor.html", {}) 
		else:
			#return render(request, "please_signup.html", {})
			return render(request, "home.html", {}) 


##########################################################################################
##########################################################################################
################## BELOW HERE ARE FEEDBACK EMAIL FUNCTIONS ###############################	
def provide_feedback(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		form_email = form.cleaned_data.get("contact_email")
		form_message = form.cleaned_data.get("message")
		if form.cleaned_data.get("username"):
			form_username = form.cleaned_data.get("username")
		else:
			form_username = 'not provided' 
		#print email, message, full_name
		subject = 'Providing General Feedback'
		from_email = settings.EMAIL_ADDR
		to_email = [from_email]
		contact_message = "username:%s___ Message: %s ____ Sent_by %s"%( 
				form_username, 
				form_message, 
				form_email)
		# some_html_message = """
		# <h1>hello</h1>
		# """
		send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, 
				#html_message=some_html_message,
				fail_silently=False)
		messages.success(request, 'Thanks! Your feedback has been submitted')
		return HttpResponseRedirect('/')
	context = {
		"form": form,
		#"messages": messages,
	}
	return render(request, "provide_feedback.html", context)

def access_issues(request):
	form = AccessIssuesForm(request.POST or None)
	if form.is_valid():
		form_email = form.cleaned_data.get("contact_email")
		form_message = form.cleaned_data.get("message")
		if form.cleaned_data.get("username"):
			form_username = form.cleaned_data.get("username")
		else:
			form_username = 'not provided' 
		subject = 'Reporting Access Issues'
		from_email = settings.EMAIL_ADDR
		to_email = [from_email]
		contact_message = "username:%s___ Message: %s ____ Sent_by %s"%( 
				form_username, 
				form_message, 
				form_email)
		send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, 
				#html_message=some_html_message,
				fail_silently=False)
		messages.success(request, 'Thanks! Your Access Issue message been submitted')
		return HttpResponseRedirect('/')
	context = {
		"form": form,
		#"messages": messages,
	}
	return render(request, "access_issues.html", context)

@login_required
def report_data_issues(request):
	form = ReportDataForm(request.POST or None)
	if form.is_valid():
		form_username = request.user
		form_email = request.user.email
		form_data_issue = form.cleaned_data.get("data_issue")
		form_practitioner_first_name = form.cleaned_data.get("practitioner_first_name")
		form_practitioner_last_name = form.cleaned_data.get("practitioner_last_name")
		form_service_area = form.cleaned_data.get("service_area")
		form_level = form.cleaned_data.get("level")
		form_office = form.cleaned_data.get("office")
		form_message = form.cleaned_data.get("message")
		subject = 'Missing/Incorrect data reported by portal user'
		from_email = settings.EMAIL_ADDR
		to_email = [from_email]
		contact_message = "data_issue:%s_ first_name:%s| last_name:%s| service_area:%s| level:%s| office:%s|  Message: %s|   Reported by: %s|	 email: %s"%( 
				form_data_issue,
				form_practitioner_first_name,
				form_practitioner_last_name,
				form_service_area,
				form_level,
				form_office,
				form_message,
				form_username, 
				form_email)
		send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, 
				#html_message=some_html_message,
				fail_silently=False)
		messages.success(request, 'Thanks for reporting missing/incorrect data. Your feedback will be reviewed soon')
		return HttpResponseRedirect('/')
	context = {
		"form": form,
		#"messages": messages,
	}
	return render(request, "report_data.html", context)

def partner_with_us(request):
	form = PartnerForm(request.POST or None)
	if form.is_valid():
		form_service_area = form.cleaned_data.get("service_ar")
		form_email = form.cleaned_data.get("contact_email")
		form_message = form.cleaned_data.get("message")
		if form.cleaned_data.get("username"):
			form_username = form.cleaned_data.get("username")
		else:
			form_username = 'not provided' 
		#print email, message, full_name
		subject = 'WANT TO PARTNER'
		from_email = settings.EMAIL_ADDR
		to_email = [from_email]
		contact_message = "username:%s___ service_area:%s___ Message: %s ____ Sent_by %s"%( 
				form_username,
				form_service_area, 
				form_message, 
				form_email)
		# some_html_message = """
		# <h1>hello</h1>
		# """
		send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, 
				#html_message=some_html_message,
				fail_silently=False)
		messages.success(request, 'Thanks! Your message has been submitted')
		return HttpResponseRedirect('/')
	context = {
		"form": form,
		#"messages": messages,
	}
	return render(request, "partner_with_us.html", context)




##############
def newuserpage(request):
	if request.user.is_authenticated() and request.user.userstatus.is_contributor:
		#Pull in the 5 most recent reviews to show folks on the homepage
		recent_reviews = Review.objects.filter(employee__is_live=True).order_by('-pk')[:5]
		#Pull in the 5 most recently likes reviews on the homepage
		recent_voted_reviews = Vote.objects.filter(employee__is_live=True).order_by('-pk')[:5]
		## count the number of reviews by user
		rev_count = request.user.review_set.count()
		## pull in all votes for each review and count them
		user_review_queryset = Review.objects.filter(user=request.user).order_by('-timestamp')
		user_review_queryset = user_review_queryset.annotate(num_votes=Count('votereview'))
		vote_ct = 0
		for obj in user_review_queryset:
				vote_ct = vote_ct + obj.num_votes
		
		context = {
		"username": request.user,  #update this
		"recent_reviews": recent_reviews,
		"recent_voted_reviews": recent_voted_reviews,
		"review_count": rev_count,
		#"vote_count": vote_count,
		#"user_review_queryset": user_review_queryset, #not needed for now, can add later
		"vote_ct": vote_ct,
		} 
		return render(request, "user_homepage.html", context)
	else:
		if request.user.is_authenticated() and request.user.userstatus.is_contributor == False:
			return render(request, "become_a_contributor.html", {}) 
		else:
			return render(request, "home.html", {})  




