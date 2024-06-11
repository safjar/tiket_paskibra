from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'transaction_id', 'order_id']  # Adjust fields as needed

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        # Disable fields that are automatically generated (user, created)
        self.fields['user'].disabled = True
        self.fields['created'].disabled = True