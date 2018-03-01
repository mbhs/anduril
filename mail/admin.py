from django.contrib import admin

from .models import Domain, Account


admin.site.register(Domain)
admin.site.register(Account)
