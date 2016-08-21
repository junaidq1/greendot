"""greendotp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include    #include pulled later on
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from . import regbackend
from reviews import views as emp 

#from reviews import views as 

#url(r'^$',   emp.go_home, name='generic_homepage'),    
#url(r'^myaccount/$', emp.goto_userpage, name='user_homepage'),

urlpatterns = [
    url(r'^siteadmin/', admin.site.urls),
    url(r'^$',   emp.goto_userpage, name='user_homepage'),    
    url(r'^about/$',   emp.about, name='about_us'),
    # url(r'^load/$',   emp.import_db, name='importdb'),   #load data into database - keep off
    #custom registration backend link
    url(r'^accounts/register/$', regbackend.MyRegistrationView.as_view(), name='registration_register'),
    
    url(r'^create0/$', emp.verify_question, name='ver_question'),   
    url(r'^myaccount/search$', emp.search_practitioner_reviews, name='search_practitioners'),
    url(r'^myaccount/myreviews/(?P<pk>\d+)/$', emp.view_past_user_reviews, name='past_user_reviews'),
    url(r'^myaccount/reviewedpractitioners/$', emp.list_of_reviewed_employees, name='reviews_longlist'),
    
    #
    url(r'^reviews/', include("reviews.urls")),
    url(r'^employees/$', emp.employee_list, name='list_of_all_employees'),
    url(r'^employees/(?P<pk>\d+)/$', emp.employee_detail, name='emp_details'),
    # url(r'^employees2/(?P<pk>\d+)/$', emp.working, name='emp_details2'),  #delete this once QA is complete
    url(r'^employees/(?P<pk>\d+)/(?P<pk2>\d+)/$', emp.vote_for_review, name='r_vote'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    #Contact_us links
    url(r'^provide_feedback/$',   emp.provide_feedback, name='provide_feedback'),
    url(r'^access_issues/$',   emp.access_issues, name='access_issues'),
    url(r'^report_data_issues/$',   emp.report_data_issues, name='report_data_issues'),
    url(r'^partner_with_us/$',   emp.partner_with_us, name='partner_with_us'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


