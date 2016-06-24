from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
#from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.


class Review(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	employee = models.ForeignKey("Employee") #in quotes because model defined later
	content = models.TextField(blank=True)
	upvotes = models.IntegerField(null=True, blank=True)
	downvotes = models.IntegerField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	WORK_AGAIN_CHOICES = (
	    ('Y', 'Yes'),
	    ('N', 'No'),
	)
	work_again =  models.CharField(verbose_name="would you work with this person again", 
									max_length=1, choices=WORK_AGAIN_CHOICES, null=False)
	#updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __unicode__(self):
		return self.content

	def get_absolute_url(self):
		return reverse("r_detail", kwargs={"pk": self.pk} )
		#return "/reviews/%s/" %(self.pk)

	class Meta:
		unique_together = (("user", "employee"),)  #really important - prevents dups
	#def create_post_step2(self):
		#return reverse("r_detail", kwargs={"pk": self.pk} )
		#return "/reviews/%s/" %(self.pk)

class Employee(models.Model):
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	email = models.CharField(max_length=120)
	level = models.CharField(max_length=120)
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
	#timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = VoteManager()

	# def __unicode__(self):
	# 	return self.user

	def __string__(self):
		return self.user
		#return unicode(self.upvotes) or u''

	# @propert
	# def vote_key(self):
	# 	return ''.join([self.review, '-', self.employee, '-', self.user])

	class Meta:
		unique_together = ("review", "employee", "user")


