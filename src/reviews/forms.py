from django import forms

from .models import Review, Employee
from registration.forms import RegistrationFormUniqueEmail #this is to edit the registration redux form

# class ReviewForm(forms.ModelForm):
# 	class Meta:
# 		model = Review
# 		fields = [
# 		"content",
# 		"employee",
# 		"work_again",
# 		]

#this form edits the registration redux form
class UserLevelRegistrationForm(RegistrationFormUniqueEmail):
	LEVEL_CHOICES = (
		('PPD', 'PPD'),
		('BA', 'BA'),
		('C', 'C'),
		('SC', 'SC'),
		('M', 'M'),
		('SM', 'SM'),
		('Other', 'other'),
	)
	level =  forms.ChoiceField(choices=LEVEL_CHOICES, label="What is your level at the firm?")

#actual review post form
class ReviewForm2(forms.ModelForm):
	class Meta:
		model = Review
		fields = [
		"length_working",
		"ques1",
		"ques2",
		"ques3",
		"work_again",
		"content",
		]

# form to validate that person signing up knows the answer to the impact day question
class ValidationForm(forms.Form):
	answer = forms.CharField()


class ContactForm(forms.Form):
	username = forms.CharField(label="Please enter your username (if applicable)", required=False)
	contact_email = forms.EmailField(label="Please provide a contact email")
	message = forms.CharField(widget=forms.Textarea)

class AccessIssuesForm(forms.Form):
	username = forms.CharField(label="Please enter your username", required=False)
	contact_email = forms.EmailField(label="Please provide a contact email")
	message = forms.CharField(label="Please describe the access issues you are having", widget=forms.Textarea)

class ReportDataForm(forms.Form):
	DataReportChoices = (
	    ('1', 'Incorrect practitioner data'),
	    ('2', 'Missing practitioner data'),
	)
	data_issue =  forms.ChoiceField(choices=DataReportChoices,
		label="What kind of data issue would you like to report?")
	practitioner_first_name = forms.CharField(label="First name of practitoner", max_length=120)
	practitioner_last_name = forms.CharField(label="Last name of practitoner", max_length=120)
	service_area = forms.CharField(label="Service Area of practitoner", max_length=120)
	level = forms.CharField(label="Level of practitoner", max_length=120)
	office = forms.CharField(label="Office of practitoner", max_length=120)
	message = forms.CharField(label="Describe data issue")




