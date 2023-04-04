from django.contrib import admin
from .models import PayHistory, Membership, UserMembership, Subscription

# Register your models here.
admin.site.register(Membership)
admin.site.register(PayHistory)
admin.site.register(UserMembership)
admin.site.register(Subscription)