from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
from slugify import slugify
from datetime import date


class CustomUser(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, unique=False)
    last_name = models.CharField(max_length=30, blank=True, unique=False)
    surname = models.CharField(max_length=30, blank=True, unique=False)
    address = models.CharField(max_length=100, blank=True, unique=False)

    def __str__(self):
        return '{}-{}-{}'.format(self.last_name, self.first_name, self.surname)


class Organization(models.Model):
    MEASUREMENT_UNITS_CHOICES = (('кВт/ч', 'кВт/ч'), ('м3', 'м3'))

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='dok_jf')
    first_name = models.CharField(max_length=100, blank=True, unique=False)
    second_name = models.CharField(max_length=100, blank=True, unique=False)
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False, unique=False)
    description = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    tariff = models.DecimalField(max_digits=4, decimal_places=2, blank=False)
    measurement_units = models.CharField(max_length=10, choices=MEASUREMENT_UNITS_CHOICES, default='')

    def save(self, *args, **kwargs):
        self.date = date.today()
        custom_slug = '{}-{}-{}'.format(self.title, self.date, self.tariff)
        # custom_slug = '{}'.format(self.title)
        self.slug = slugify(custom_slug)
        # self.difference = self.current_counter_value - self.previous_counter_value
        # self.amount = self.difference * self.organization.tariff
        super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='dok_jf')
    date = models.DateField(auto_now_add=True)
    # slug = models.SlugField(max_length=100, unique=True, blank=True)
    difference = models.PositiveIntegerField(default=0, blank=True, null=True)
    amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_fk')
    previous_counter_value = models.PositiveIntegerField(default=0, blank=True, null=False)
    current_counter_value = models.PositiveIntegerField(default=0, blank=False, null=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        self.date = date.today()
        return '{}-{}'.format(self.organization, self.date)
