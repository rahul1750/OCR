from django.contrib import admin
from django.contrib import messages
from .models import Product, Category, Client, Order
from django.core.exceptions import ValidationError

# Register your models here.
admin.site.register(Category)
admin.site.register(Order)


@admin.action(description='Add 50 to the stock')
def add_fifty(modeladmin, request, queryset):
    CRITICAL = 50
    for ele in queryset:
        ele.stock = ele.stock + 50
        if ele.stock > 0:
            ele.available = True
        if ele.stock > 1000 or ele.stock < 0:
            messages.error(request, 'Stock must be inbetween 1 and 1000 in ' + ele.name)

        else:
            ele.save()


# Features Task 1:
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "available")
    actions = [add_fifty]


# Features Task 9
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "city", "get_interested_in")

    def get_interested_in(self, obj):
        return ",\n".join([cat.name for cat in obj.interested_in.all()])
