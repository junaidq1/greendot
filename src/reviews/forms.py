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
		"content",
		"work_again",
		]