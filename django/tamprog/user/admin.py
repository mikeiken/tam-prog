from django.contrib import admin
from .models import *



admin.site.register(Worker)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'phone_number', 'wallet_balance', 'is_active', 'is_staff')
    search_fields = ('username', 'full_name', 'phone_number')
    list_filter = ('is_staff', 'is_active')
admin.site.register(Person, PersonAdmin)