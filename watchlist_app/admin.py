from django.contrib import admin
from .models import WatchList,StreamPlatform,Review

admin.site.register(WatchList)
admin.site.register(StreamPlatform)
admin.site.register(Review)