from django.contrib import admin
from .models import *

# admin.site.register(Organization)
# admin.site.register(Payment)
# admin.site.register(Order)
# admin.site.register(PaymentInOrder)
# admin.site.register(CustomUser)


class PaymentInOrderInline(admin.TabularInline):
    model = PaymentInOrder


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomUser._meta.fields]

    class Meta:
        model = CustomUser
# admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Organization._meta.fields]

    class Meta:
        model = Organization


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields]

    class Meta:
        model = Payment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [PaymentInOrderInline]

    class Meta:
        model = Order


@admin.register(PaymentInOrder)
class PaymentInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PaymentInOrder._meta.fields]

    class Meta:
        model = PaymentInOrder
