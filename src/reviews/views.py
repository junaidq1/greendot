from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .models import Review, Employee, Vote, VoteManager
from .forms import ReviewForm, ReviewForm2, ValidationForm
from django.db.models import Q
from django.contrib.auth.models import User #test this guy - remove if needed
from django.db.models import Count, Sum
from django.core.mail import send_mail
# Create your views here.


def go_home(request):	
	return render(request, "home.html", {})


def review_list(request):
	queryset = Review.objects.all()

	if request.user.is_authenticated():
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


def review_create1(request):
	queryset_list = Employee.objects.all()
	query = request.GET.get("q1")
	if query:  #add an or here
		queryset_list = queryset_list.filter(
						Q(last_name__icontains=query)
						)
		print queryset_list
	context = {
	"queryset_list":queryset_list,
	"query": query
	}
	return render(request, "create_review1.html", context)
		#return HttpResponseRedirect('/reviews/create2/')


def review_create2(request, pk=None):
	#form = ReviewForm(request.POST or None)
	#instance = get_object_or_404(Review, pk=pk) #this is what was working_1
	#form = ReviewForm(request.POST or None, instance=instance) #this is what was working_2	
	form = ReviewForm2(request.POST or None)
	obj = Employee.objects.get(pk=pk)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.employee = Employee.objects.get(pk=pk)
		instance.user = request.user
		instance.save()
		return HttpResponseRedirect('/reviews/create3/')
	context = {
		"form": form,
		"obj": obj,
	}
	return render(request, "create_review2.html", context)

def review_create3(request):
	return render(request, "create_review3.html", {})


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


def employee_list(request):
	queryset = Employee.objects.all()

	if request.user.is_authenticated():
		context = {"obj_list": queryset}
	else:
		context = {"title": "Unauthenticated List"}
	return render(request, "employee_list.html", context) 

# def employee_detail(request, pk=None):
# 	instance = get_object_or_404(Employee, pk=pk)
# 	rev_list = instance.review_set.all()
# 	context = {
# 		"review_list": rev_list,
# 		"instance": instance
# 	}
# 	return render(request, "employee_detail.html", context)

def employee_detail(request, pk=None):
	instance = get_object_or_404(Employee, pk=pk)
	rev_list = instance.review_set.all() #.order_by("-count('upvotes')")
	#rev_list = instance.review_set.all().annotate(num_votes=Count('upvotes')).order_by('-num_votes')
	rev_list = rev_list.annotate(num_votes=Count('votereview')).order_by('-num_votes')
	print rev_list
	#vote_list = instance.vote_set.all()
	#vote_list = instance.
	context = {
		"review_list": rev_list,
		"instance": instance,
		#"vote_list": vote_list,
	}
	return render(request, "employee_detail.html", context)


# def working(request, pk=None):
# 	instance = get_object_or_404(Employee, pk=2)
# 	rev_list = instance.review_set.all()
# 	#vote_list = instance.vote_set.all()
# 	#vote_list = instance.
# 	context = {
# 		"review_list": rev_list,
# 		"instance": instance,
# 		#"vote_list": vote_list,
# 	}
# 	return render(request, "working.html", context)


def vote_for_review(request, pk=None, pk2=None):
	emp_instance = get_object_or_404(Employee, pk=pk)
	rev_instance = get_object_or_404(Review, pk=pk2)
	#print emp_instance
	#print rev_instance
	if request.user.is_authenticated():
		us = request.user
		Vote.objects.create(user = us, review=rev_instance, employee= emp_instance, upvotes=True) 
		#content=cont, employee=Employee.objects.get(pk=emp))
		vote_status = "successfully"
	else:
		vote_status = "unsuccessfully"
	context = {
		"vote_status": vote_status
	}		
	return render(request, "voted.html", context)	




