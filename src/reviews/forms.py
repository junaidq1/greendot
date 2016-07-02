from django import forms

from .models import Review, Employee


class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = [
		"content",
		"employee",
		"work_again",
		]

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


class ValidationForm(forms.Form):
	answer = forms.CharField()