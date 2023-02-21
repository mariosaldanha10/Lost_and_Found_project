from django.contrib import admin
from assets.models import ItemInfo, RequestInfo, ClaimInfo, UserProfile

# Register your models here.

admin.site.register(ItemInfo)
admin.site.register(RequestInfo)
admin.site.register(ClaimInfo)
admin.site.register(UserProfile)