from django.contrib import admin
from .models import *

# Register your models here.

# class ListingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'img_url', 'owner', 'category')    


admin.site.register(User)
admin.site.register(Listings)
# admin.site.register(Listings, ListingAdmin)
admin.site.register(Bids)
admin.site.register(WatchList)
# admin.site.register(Comments)
