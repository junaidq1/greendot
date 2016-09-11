
from django import forms

from .models import Wishlist, Fvote

class Create_wishlist_item(forms.ModelForm):
	class Meta:
		model = Wishlist
		fields = ["feature"]
