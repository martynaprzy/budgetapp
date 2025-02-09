from django.contrib import admin
from .models import Expense, Category, Income, Budget

admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(Income)
admin.site.register(Budget)