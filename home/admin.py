from django.contrib import admin
from .models import Song, Artist, Album, PlayList, PlayListSong, ListenCount

admin.site.register(Song)
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(PlayListSong)
admin.site.register(PlayList)
admin.site.register(ListenCount)
