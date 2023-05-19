from django.contrib import admin

from .models import *

# Register your models here.


admin.site.register(User)
admin.site.register(Music)
admin.site.register(PlaylistMusic)
admin.site.register(PlaylistUser)
admin.site.register(Playlist)
admin.site.register(Favourite)