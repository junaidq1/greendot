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

from reviews import views as emp 

#from reviews import views as 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',   emp.go_home, name='going_home_page'),
    
    url(r'^reviews/', include("reviews.urls")),
    url(r'^employees/$', emp.employee_list, name='fsdfasdfds'),
    url(r'^employees/(?P<pk>\d+)/$', emp.employee_detail, name='emp_details'),
    # url(r'^employees2/(?P<pk>\d+)/$', emp.working, name='emp_details2'),  #delete this once QA is complete
    url(r'^employees/(?P<pk>\d+)/(?P<pk2>\d+)/$', emp.vote_for_review, name='r_vote'),
    url(r'^accounts/', include('registration.backends.default.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


