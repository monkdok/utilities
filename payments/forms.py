from django import forms
from django.contrib.auth.models import User

from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class OrganizationCreateForm(forms.ModelForm):
     class Meta:
          model = Organization
          fields = [
              'title',
              'tariff',
              'measurement_units',
          ]
          # exclude = ['']


class PaymentCreateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            # 'organization',
            'previous_counter_value',
            'current_counter_value',
        ]