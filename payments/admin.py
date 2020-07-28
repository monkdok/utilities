from django.contrib import admin
from .models import *

# admin.site.register(Organization)
# admin.site.register(Payment)
# admin.site.register(Order)
# admin.site.register(PaymentInOrder)
# admin.site.register(CustomUser)
# admin.site.register(Icons)


class PaymentInCartInline(admin.TabularInline):
    model = PaymentInCart


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


@admin.register(Icons)
class IconsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icons._meta.fields]

    class Meta:
        model = Icons
        

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields]

    class Meta:
        model = Payment   
        
             
@admin.register(PaymentInCart)
class PaymentInCartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PaymentInCart._meta.fields]

    class Meta:
        model = PaymentInCart


# @admin.register(PaymentInOrder)
# class PaymentInOrderAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in PaymentInOrder._meta.fields]
#
#     class Meta:
#         model = PaymentInOrder



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [PaymentInCartInline]

    class Meta:
        model = Order
