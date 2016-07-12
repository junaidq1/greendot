
from registration.backends.default.views import RegistrationView
from reviews.forms import UserLevelRegistrationForm
from reviews.models import UserLevel


#JQ: custom registration form
# class MyRegistrationView(RegistrationView):

# 	form_class = UserLevelRegistrationForm

# 	def register(self, form):
# 		print 'nahi'
# 		new_user = super(MyRegistrationView, self).register(self, form) #form_class
# 		user_profile = UserLevel()
# 		user_profile.user = new_user
# 		user_profile.level = form_class.cleaned_data['level']
# 		print 'goblin'
# 		user_profile.save()
# 		return user_profile
# 		#return super(MyRegistrationView, self).form_valid(request, form)

class MyRegistrationView(RegistrationView):

	form_class = UserLevelRegistrationForm

	def register(self, form_class):
	    print 'test'
	    new_user = super(MyRegistrationView, self).register(form_class)
	    user_profile = UserLevel()
	    user_profile.user = new_user
	    user_profile.level = form_class.cleaned_data['level']
	    user_profile.save()
	    return user_profile