from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Query)
admin.site.register(WorldMap)
admin.site.register(WordCloud)
admin.site.register(TopConversations)
