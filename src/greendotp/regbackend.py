
from registration.backends.default.views import RegistrationView
from reviews.forms import UserLevelRegistrationForm
from reviews.models import UserLevel



#this reg backend was built to customize the form that a user sees when they try to register for an account

class MyRegistrationView(RegistrationView):

	form_class = UserLevelRegistrationForm

	def register(self, form_class):
	    new_user = super(MyRegistrationView, self).register(form_class)
	    user_profile = UserLevel()
	    user_profile.user = new_user
	    user_profile.level = form_class.cleaned_data['level']
	    user_profile.office = form_class.cleaned_data['office']
	    user_profile.service_area = form_class.cleaned_data['service_area']
	    user_profile.save()
	    return user_profile