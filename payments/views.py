from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from datetime import date
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View, DetailView, DeleteView, UpdateView
from .forms import *
from fpdf import FPDF


class CustomUserView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request):
        form = CustomUserForm()
        context = {
            'form': form,
        }
        return render(request, 'payments/personal_data.html', context)

    def post(self, request):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = self.request.user
            print('BEFORE SAVE')
            form.save()
            print('user==========', form)
            return redirect('organization_list_url')
        else:
            print('NOT VALID')


class OrganizationCreate(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request):
        icons = Icons.objects.all()
        form = OrganizationCreateForm()
        context = {
            'icons': icons,
            'form': form,
        }
        return render(request, 'payments/organization_create.html', context)

    def post(self, request):
        form = OrganizationCreateForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = self.request.user
            form.save()
            return redirect('organization_list_url')
        return HttpResponseRedirect(self.request.path_info)


class OrganizationList(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request):
        if CustomUser.objects.all():
            user = CustomUser.objects.get(user=self.request.user)
        else:
            user = None
        services = Organization.objects.filter(author=self.request.user)
        context = {
            'services': services,
            'user': user,
        }
        return render(request, 'payments/organization_list.html', context)


class OrganizationDetail(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request, slug):
        form = OrganizationCreateForm()
        if CustomUser.user == request.user:
            user = CustomUser.objects.get(user=self.request.user)
        else:
            user = None
        organization = Organization.objects.get(author=self.request.user, slug=slug)
        payments = Payment.objects.filter(author=self.request.user, organization=organization)
        if len(payments) > 0:
            last_payment = payments.latest('id')
        else:
            last_payment = None
        context = {
            # 'user': user,
            'organization': organization,
            'form': form,
            'payments': payments,
            'last_payment': last_payment,

        }
        return render(request, 'payments/organization_detail.html', context)


# class OrganizationUpdate(LoginRequiredMixin, UpdateView):
#     login_url = 'account_login'
#     model = Organization
#     template_name = 'payments/organization_update.html'
#     form_class = OrganizationCreateForm
#
#     def get_success_url(self):
#         return reverse('organization_detail_url', kwargs={'slug': self.object.slug})
#         # return reverse('organization_detail_url', kwargs={'slug': self.object.slug})
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in a QuerySet of all the books
#         context['icons'] = Icons.objects.all()
#         return context

class OrganizationUpdate(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request, slug):
        form = OrganizationCreateForm()
        icons = Icons.objects.all()
        service = Organization.objects.get(author=self.request.user, slug=slug)
        # user = CustomUser.objects.get(user=self.request.user)
        context = {
            'form': form,
            'icons': icons,
            'service': service,
        }
        return render(request, 'payments/organization_update.html', context)

    def post(self, request, slug):
        service = Organization.objects.get(author=self.request.user, slug=slug)
        form = OrganizationCreateForm(request.POST or None, instance=service)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('organization_detail_url', kwargs={'slug': form.instance.slug}))
            # return HttpResponseRedirect(self.request.path_info)
        return HttpResponseRedirect(reverse('organization_update_url', kwargs={'slug': form.instance.slug}))


class OrganizationDelete(LoginRequiredMixin, DeleteView):
    login_url = 'account_login'
    model = Organization
    template_name = 'payments/organization_delete.html'

    def get_success_url(self):
        return reverse('organization_list_url')


class PaymentCreate(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request, slug):
        form = PaymentCreateForm()
        organization = Organization.objects.get(slug=slug)
        payments = Payment.objects.filter(organization=organization)
        payment_period = date.today()
        if len(payments) > 0:
            last_payment = Payment.objects.latest('id')
        else:
            last_payment = None
        context = {
            'form': form,
            'organization': organization,
            'last_payment': last_payment,
            'payment_period': payment_period,
        }
        return render(request, 'payments/payment_create.html', context)

    def post(self, request, slug):
        form = PaymentCreateForm(request.POST)
        organization = Organization.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.organization = organization
            if form.current_counter_value > form.previous_counter_value:
                form.difference = form.current_counter_value - form.previous_counter_value
                form.price = form.difference * organization.tariff
            form.author = self.request.user
            form.save()
            return HttpResponseRedirect(reverse('payment_detail_url', kwargs={'pk': form.id}))
        else:
            print('=================not valid')


class PaymentList(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request):
        organization = Organization.objects.all()
        form = OrganizationCreateForm()
        context = {
            'organization': organization,
            'form': form,
        }
        return render(request, 'payments/organization_list.html', context)


class PaymentDetail(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request, pk):
        payment = Payment.objects.get(id=pk)
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        context = {
            'payment': payment,

        }
        return render(request, 'payments/payment_detail.html', context)


class PaymentArchive(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request, slug):
        organization = Organization.objects.get(slug=slug)
        payments = Payment.objects.filter(organization=organization)
        context = {
            'payments': payments,
            'organization': organization,
        }
        return render(request, 'payments/payment_archive.html', context)


class PaymentUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'account_login'
    model = Payment
    template_name = 'payments/Payment_update.html'
    form_class = PaymentCreateForm

    def get_success_url(self):
        return reverse('payment_list_url')


class PaymentDelete(LoginRequiredMixin, DeleteView):
    login_url = 'account_login'
    model = Payment
    template_name = 'payments/payment_delete.html'

    def get_success_url(self):
        return reverse('organization_list_url')


class CartAdding(View):

    def post(self, request, pk):
        data = {}
        session_key = request.session.session_key
        payment = Payment.objects.get(pk=pk)
        new_payment, created = PaymentInCart.objects.get_or_create(session_key=session_key, payment_id=pk, is_ordered=False)
        total_payments = PaymentInCart.objects.filter(session_key=session_key, is_ordered=False).count()
        payments_in_cart = PaymentInCart.objects.filter(session_key=session_key, is_ordered=False)
        if not created:
            data['exist'] = True
        else:
            data['exist'] = False
        context = {
            'payment': new_payment,
            'payments': payments_in_cart,
        }
        data['payment'] = render_to_string('payments/snippets/append_to_cart.html', context, request)
        data['count'] = total_payments
        return JsonResponse(data)


class CartItemDelete(View):

    def post(self, request):
        data = {}
        session_key = request.session.session_key
        is_delete = request.POST.get('is_delete')
        pk = request.POST.get('pk')
        payment_in_cart_to_delete = PaymentInCart.objects.get(pk=pk)
        payment_in_cart_to_delete.delete()
        total_payments = PaymentInCart.objects.filter(session_key=session_key, is_ordered=False).count()
        data['deleted'] = True
        data['count'] = total_payments
        return JsonResponse(data)


class Checkout(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request):
        session_key = request.session.session_key
        payments = PaymentInCart.objects.filter(session_key=session_key, is_ordered=False)
        context = {
            'payments': payments,
        }
        return render(request, 'payments/checkout.html', context)

    def post(self, request):
        data = request.POST
        order = Order.objects.create(author=self.request.user)
        session_key = request.session.session_key
        payments = PaymentInCart.objects.filter(session_key=session_key, is_ordered=False)
        total_price = 0
        for name, value in data.items():
            if name != 'csrfmiddlewaretoken':
                payment = PaymentInCart.objects.get(id=value)
                total_price += payment.payment.price
                payment.order = order
                payment.is_ordered = True
                payment.save()
        order.total_price = total_price
        order.save()
        return redirect('organization_list_url')


class ProfileSettings(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request):
        user = CustomUser.objects.get(user=self.request.user)
        temp = 'profile'
        context = {
            'user': user,
        }
        return render(request, 'payments/profile_settings.html', context)


class OrderDetailView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        context = {
            'order': order,
        }
        return render(request, 'payments/order_detail.html', context)


class IconSelect(View):

    def get(self, request):
        data = {}
        pk = request.GET['pk']
        icon = Icons.objects.get(pk=pk)
        context = {'icon': icon}
        data['html'] = render_to_string('payments/snippets/icon_preview.html', context, request)
        return JsonResponse(data)
