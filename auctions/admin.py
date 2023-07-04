from django.contrib import admin
from .models import *

# Register your models here.
class AuctionListingAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(AuctionListing,AuctionListingAdmin)
admin.site.register(WatchListModel)
admin.site.register(AuctionBidsModel)
admin.site.register(CommentsModel)
admin.site.register(User)
