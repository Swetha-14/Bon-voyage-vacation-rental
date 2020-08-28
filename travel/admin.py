from django.contrib import admin
from .models import *

class PlaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title',  'price', 'city','address', 'created_date']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'place', 'guests', 'checkin_date', 'checkout_date']



# Register your models here.
admin.site.register(User)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Images)
admin.site.register(Comment)
admin.site.register(Saved)