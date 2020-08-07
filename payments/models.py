# from unittest import signals
from django.db.models.signals import post_save
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
        return '{} {} {}'.format(self.last_name, self.first_name, self.surname)


class Icons(models.Model):
    icon = models.ImageField(upload_to='img/icons/', default=None)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Icon'
        verbose_name_plural = 'Icons'


class Organization(models.Model):
    MEASUREMENT_UNITS_CHOICES = (('кВт/ч', 'кВт/ч'), ('м3', 'м3'))
    # ICON_CHOICES = (
    #     ('app.png', 'app.png'),
    #     ('archive-3.png', 'archive-3.png'),
    #     ('smiley_happy.png', 'happy happy joy joy'),
    # )

    id = models.AutoField(primary_key=True)
    icon = models.ForeignKey(Icons, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT, related_name='organization')
    # icon = models.CharField(max_length=100, choices=ICON_CHOICES, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default='')
    first_name = models.CharField(max_length=100, blank=True, unique=False)
    second_name = models.CharField(max_length=100, blank=True, unique=False)
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False, unique=False)
    description = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    tariff = models.DecimalField(max_digits=7, decimal_places=2, blank=False)
    measurement_units = models.CharField(max_length=10, choices=MEASUREMENT_UNITS_CHOICES, default='')

    def save(self, *args, **kwargs):
        self.date = date.today()
        custom_slug = '{}-{}-{}'.format(self.title, self.date, self.tariff)
        self.slug = slugify(custom_slug)
        super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Order(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, related_name='orders')
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.created = date.today()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return '#{}({})'.format(self.id, self.created)


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='', null=True)
    date = models.DateField(auto_now_add=True)
    payment_period = models.CharField(max_length=10, blank=True, unique=False)
    difference = models.PositiveIntegerField(default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='payment')
    previous_counter_value = models.PositiveIntegerField(default=0, blank=True, null=False)
    current_counter_value = models.PositiveIntegerField(default=0, blank=False, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment', default='', null=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        self.date = date.today()
        return '{}-{}'.format(self.organization, self.date)


# class PaymentInOrder(models.Model):
#     order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
#     payment = models.ForeignKey(Payment, blank=True, null=True, default=None, on_delete=models.CASCADE)
#     price_per_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     created = models.DateTimeField(auto_now_add=True, auto_now=False)
#     updated = models.DateTimeField(auto_now_add=False, auto_now=True)
#
#     def __str__(self):
#         created = date.today()
#         self.created = '{}-{}-{}'.format(created.day, created.month, created.year)
#         return '{}-{}'.format(self.payment.organization.title, self.created)
#
#     def save(self, *args, **kwargs):
#         self.created = '{}-{}-{}'.format(date.day, date.month, date.year)
#         self.price_per_payment = self.payment.price
#         super(PaymentInOrder, self).save(*args, **kwargs)
#
#
# def payment_in_order_post_save(sender, instance, **kwargs):
#     order = instance.order
#     all_payments_in_order = PaymentInOrder.objects.filter(order=order)
#     order_total_price = 0
#     for payment in all_payments_in_order:
#         order_total_price += payment.price_per_payment
#     order.total_price = order_total_price
#     order.save(force_update=True)
#
#
# post_save.connect(payment_in_order_post_save, PaymentInOrder)


class PaymentInCart(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT, related_name='payments_in_cart')
    payment = models.ForeignKey(Payment, blank=True, null=True, default=None, on_delete=models.CASCADE, related_name='payment_in_cart')
    price_per_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_ordered = models.BooleanField(default=False, null=True)

    def __str__(self):
        created = date.today()
        self.created = '{}-{}-{}'.format(created.year, created.month, created.day)
        return '{}-{}'.format(self.payment.organization.title, self.created)

    def save(self, *args, **kwargs):
        created = date.today()
        self.created = '{}-{}-{}'.format(created.year, created.month, created.day)
        self.price_per_payment = self.payment.price
        super(PaymentInCart, self).save(*args, **kwargs)


