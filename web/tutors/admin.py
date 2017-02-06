from django.contrib import admin

# Register your models here.

from .models import Subject, Language, Offer, Request

admin.site.register(Subject)
admin.site.register(Language)
admin.site.register(Offer)
admin.site.register(Request)
