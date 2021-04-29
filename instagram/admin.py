from django.contrib import admin
from .models import Posts, Profile,Comments


admin.site.register(Profile)
admin.site.register(Posts)
admin.site.register(Comments)


