from django import forms
from . import models

class CreateWishlist(forms.ModelForm):
    class Meta:
        model = models.BarangWishlist
        fields = '__all__'