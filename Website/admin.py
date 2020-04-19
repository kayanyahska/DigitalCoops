from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Item, Review, UserProfile, Transactions, ItemSold, CartItem, Category

# Register your models here.

#admin.site.register(Item)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'item_id', 'unit_price', 'status')


#admin.site.register(Review)
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ('title', 'product', 'review_date', 'user')

admin.site.register(UserProfile)
admin.site.register(Transactions)
admin.site.register(ItemSold)
admin.site.register(CartItem)
admin.site.register(Category)