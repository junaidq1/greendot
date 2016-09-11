from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator


# Create your models here.
class Wishlist(models.Model):
	feature = models.CharField(max_length=100)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	f_timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	

	def __unicode__(self):
		return self.feature

	def __string__(self):
		return self.user
		#return unicode(self.upvotes) or u''

	class Meta:
		unique_together = ("feature", "user")

class Fvote(models.Model):
	feature = models.ForeignKey(Wishlist, related_name='featurewishlist' )
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	feature_votes = models.BooleanField(default=True)
	fv_timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	#timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	# def __unicode__(self):
	# 	return self.feature_votes

	def __string__(self):
		return self.user
		#return unicode(self.upvotes) or u''
		
	class Meta:
		unique_together = ("feature", "user", "feature_votes")