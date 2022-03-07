from django.contrib import admin

from .models import User, Customer, Product, Expense, Category, Income, AgentSalesProduct

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(AgentSalesProduct)
