from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
#from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator 
# Create your models here.


class Review(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	employee = models.ForeignKey("Employee") #in quotes because model defined later
	length_working = models.PositiveIntegerField(verbose_name="how long have you worked with this person? (months)?")
	ques1 = models.PositiveIntegerField(verbose_name="How much did you enjoy working with this person (1-5)? (5 = most)?", validators=[MinValueValidator(1), MaxValueValidator(5)])
	ques2 = models.PositiveIntegerField(verbose_name="How much did you learn from this individual while working with them (1-5)? (5 = most)", validators=[MinValueValidator(1), MaxValueValidator(5)])
	ques3 = models.PositiveIntegerField(verbose_name="How competent is this person in their domain of expertise (1-5)? (5 = most)", validators=[MinValueValidator(1), MaxValueValidator(5)])
	#upvotes = models.IntegerField(null=True, blank=True)
	#downvotes = models.IntegerField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	WORK_AGAIN_CHOICES = (
	    ('Y', 'Yes'),
	    ('N', 'No'),
	)
	work_again =  models.CharField(verbose_name="would you work with this person again if you had the choice?", 
									max_length=1, choices=WORK_AGAIN_CHOICES, null=False)
	content = models.TextField(verbose_name="Please provide some comments on what it was like to work with this person", 
									max_length=1500)
	#updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __unicode__(self):
		return self.content

	def get_absolute_url(self):
		return reverse("r_detail", kwargs={"pk": self.pk} )
		#return "/reviews/%s/" %(self.pk)

	class Meta:
		unique_together = (("user", "employee"),)  #really important - prevents dups


class Employee(models.Model):
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	email = models.CharField(max_length=120)
	level = models.CharField(max_length=120)
	service_area = models.CharField(max_length=120)
	office = models.CharField(max_length=120)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	@property
	def full_name(self):
		return ''.join([self.last_name, ', ', self.first_name])

	def __unicode__(self):
		return self.full_name

class VoteManager(models.Manager):
	def fupvotes(self):
		return super(VoteManager, self).filter(upvotes=True)

class Vote(models.Model):
	review = models.ForeignKey(Review,related_name='votereview' )
	employee = models.ForeignKey(Employee, related_name='employeevoted')
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	upvotes = models.NullBooleanField()
	downvotes = models.NullBooleanField()
	v_timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	#timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = VoteManager()

	# def __unicode__(self):
	# 	return self.user

	def __string__(self):
		return self.user
		#return unicode(self.upvotes) or u''
		
	class Meta:
		unique_together = ("review", "employee", "user")


#this is an extension of the user model to basically ensure that the user
# has atleast contributed once before they can see the content on the site
class UserStatus(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_contributor = models.BooleanField(default=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def get_contr_status(self):
	    # The user is identified by their email address
	    return self.is_contributor

	def __string__(self):
		return self.is_contributor


#this is the signal receiver that creates a new model instance for User status
def userstatus_post_save_receiver(sender, **kwargs):
	user = kwargs["instance"]
	if kwargs["created"]:
		user_status = UserStatus(user=user, is_contributor=False)
		user_status.save()

#post save signal to create a UserStatus instance every time a new user is built
post_save.connect(userstatus_post_save_receiver, sender=User)


#this is signal receiver that changes the contributed status of a user after they submit a review
def update_contributor_status_receiver(sender, instance, **kwargs):
	user = instance.user
	UserStatus.objects.filter(user=user).update(is_contributor=True)

#this is a post save signal generator once a user submits a review
post_save.connect(update_contributor_status_receiver, sender=Review)

