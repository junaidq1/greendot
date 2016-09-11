from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Wishlist, Fvote
from .forms import Create_wishlist_item
from django.db.models import Q
from django.contrib.auth.models import User #test this guy - remove if needed
from django.db.models import Count, Sum, Avg
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib import messages
# Create your views here.
 
@login_required
def see_wishlist(request):
	form = Create_wishlist_item(request.POST or None)
	if form.is_valid():
		try:
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			#return HttpResponseRedirect('/reviews/create3/')
			form = Create_wishlist_item() #empty form to clear the box after hitting submit
		except:
			return HttpResponseRedirect('/wishlist/error/')
	queryset = Wishlist.objects.all()
	
	wishlist_queryset = Wishlist.objects.all().order_by('-f_timestamp')
	#review_votes = user_review_queryset.annotate(num_votes=Count('votereview'))
	wishlist_queryset = wishlist_queryset.annotate(num_votes=Count('featurewishlist')).order_by('-num_votes')

	context = {
	"form": form,
	"queryset":queryset,
	"wishlist_queryset": wishlist_queryset,
	# "query": query
	}
	print queryset
	return render(request, "feature_wishlist_page.html", context)
		#return HttpResponseRedirect('/reviews/create2/')


@login_required
def vote_for_feature(request, pk=None):
	feature_instance  = get_object_or_404(Wishlist, pk=pk)
	#print emp_instance
	#print rev_instance
	vote_status = "unsuccessfully"
	if request.user.is_authenticated():
		try:
			us = request.user
			Fvote.objects.create(user = us, feature=feature_instance) 
			#content=cont, employee=Employee.objects.get(pk=emp))
			vote_status = "successfully"
		except:
			return HttpResponseRedirect('/wishlist/error/')
	context = {
		"vote_status": vote_status
	}		
	return render(request, "voted.html", context)

def wishl_error(request):	
	return render(request, "wishlist_error.html", {})



