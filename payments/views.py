from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View, DetailView, DeleteView, UpdateView
from .forms import *


class OrganizationList(View):
    def get(self, request):
        organization = Organization.objects.all()
        form = OrganizationCreateForm()
        context = {
            'organization': organization,
            'form': form,
        }
        return render(request, 'payments/organization_list.html', context)

    def post(self, request):
        form = OrganizationCreateForm(request.POST)
        if form.is_valid():
            # form = form.save(commit=False)
            # form.author = self.request.user
            print('inside is form is valid')
            form.save()
            return HttpResponseRedirect(self.request.path_info)
        else:
            print('not valid')


class OrganizationDetail(View):
    def get(self, request, slug):
        form = OrganizationCreateForm()
        organization = Organization.objects.get(slug=slug)
        payments = Payment.objects.filter(organization=organization)
        if len(payments) > 0:
            last_payment = Payment.objects.latest('id')
        else:
            last_payment = None
        context = {
            'organization': organization,
            'form': form,
            'payments': payments,
            'last_payment': last_payment,

        }
        return render(request, 'payments/organization_detail.html', context)


class OrganizationUpdate(UpdateView):
    model = Organization
    template_name = 'payments/organization_update.html'
    form_class = OrganizationCreateForm

    def get_success_url(self):
        return reverse('organization_list_url')


class OrganizationDelete(DeleteView):
    model = Organization
    template_name = 'payments/organization_delete.html'

    def get_success_url(self):
        return reverse('organization_list_url')


class PaymentCreate(View):
    def get(self, request, slug):
        form = PaymentCreateForm()
        organization = Organization.objects.get(slug=slug)
        payments = Payment.objects.filter(organization=organization)
        if len(payments) > 0:
            last_payment = Payment.objects.latest('id')
        else:
            last_payment = None
        context = {
            'form': form,
            'organization': organization,
            'last_payment': last_payment,
        }
        return render(request, 'payments/payment_create.html', context)

    def post(self, request, slug):
        form = PaymentCreateForm(request.POST)
        organization = Organization.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.organization = organization
            if form.current_counter_value and form.previous_counter_value:
                form.difference = form.current_counter_value - form.previous_counter_value
                form.amount = form.difference * organization.tariff
            print('organization:', organization)
            print('difference:', form.difference)
            print('amount:', form.amount)
            # form.author = self.request.user
            form.save()
            return redirect('organization_list_url')
        else:
            print('=================not valid')


class PaymentList(View):
    def get(self, request):
        organization = Organization.objects.all()
        form = OrganizationCreateForm()
        context = {
            'organization': organization,
            'form': form,
        }
        return render(request, 'payments/organization_list.html', context)


class PaymentDetail(View):
    def get(self, request, pk):
        payment = Payment.objects.get(id=pk)
        organization = payment.organization
        context = {
            'payment': payment,

        }
        return render(request, 'payments/payment_detail.html', context)


class PaymentArchive(View):
    def get(self, request, slug):
        organization = Organization.objects.get(slug=slug)
        payments = Payment.objects.filter(organization=organization)
        context = {
            'payments': payments,
            'organization': organization,
        }
        return render(request, 'payments/payment_archive.html', context)
