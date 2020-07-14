from django import forms
from django.contrib.auth.models import User

from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from allauth.account.forms import SignupForm


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
            'payment_period',
        ]


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'surname',
            'address',

        ]


# class CustomSignupForm(SignupForm):
#     first_name = forms.CharField(max_length=30, label='First Name')
#     last_name = forms.CharField(max_length=30, label='Last Name')
#
#     def signup(self, request, user):
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.save()
#         return user
