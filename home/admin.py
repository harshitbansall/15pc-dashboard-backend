from django.contrib import admin

from .models import *

# class Balance_Admin(admin.ModelAdmin):
#     list_display = ('user','amount','created_at','id')
#     readonly_fields = ('id',)

class Payment_Admin(admin.ModelAdmin):
    list_display = ('user','amount','created_at','id')
    readonly_fields = ('id',)

# admin.site.register(Balance, Balance_Admin) 
admin.site.register(Payment, Payment_Admin) 