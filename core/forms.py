from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Оставьте комментарий (необязательно)",
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "comment": "Комментарий",
        }
