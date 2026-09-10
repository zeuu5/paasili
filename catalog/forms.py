from django import forms
from django.core.validators import RegexValidator

from .models import DealerRegistration


class DealerRegistrationForm(forms.ModelForm):
    gst_number = forms.CharField(
        label="GST number",
        max_length=15,
        required=True,
        validators=[RegexValidator(r"^[0-9A-Za-z]{15}$", "Enter a valid 15-character GST number.")],
    )

    class Meta:
        model = DealerRegistration
        fields = ("business_name", "contact_name", "city", "gst_number", "phone", "email")
        labels = {
            "business_name": "Company name",
            "contact_name": "Representative name",
            "email": "Company email",
        }
        widgets = {
            "business_name": forms.TextInput(attrs={"placeholder": "Your registered company name"}),
            "contact_name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
            "gst_number": forms.TextInput(attrs={"placeholder": "15-character GST number", "maxlength": "15"}),
            "phone": forms.TextInput(attrs={"placeholder": "+91 98765 43210", "type": "tel"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@company.com"}),
        }
