from django.contrib import admin
from .models import Listing, Bid, Comment, Status

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Status)