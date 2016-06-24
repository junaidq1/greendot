
from django.conf.urls import url
from django.contrib import admin

#from reviews import views as 
from .views import (
	review_list, 
	#review_create, 
	review_detail, 
	#review_update, 
	review_delete, 
	review_create1, 
	review_create2, 
	review_create3,
	)

urlpatterns = [
    #url(r'^$', "reviews.views.review_list"),
    url(r'^$', review_list, name='all_reviews'),
    #url(r'^create/$', review_create),
    url(r'^(?P<pk>\d+)/$', review_detail, name='r_detail'),
    #url(r'^(?P<pk>\d+)/edit/$', review_update, name='r_update'),
    url(r'^delete/$', review_delete),
    url(r'^create1/$', review_create1),
    url(r'^create2/(?P<pk>\d+)/$', review_create2, name='create_step2'),
    url(r'^create3/$', review_create3, name='create_step3'),

]
