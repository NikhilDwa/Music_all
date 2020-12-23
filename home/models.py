from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class PlayList(models.Model):
    playlist_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User)
    playlist_name = models.CharField(max_length=100, default="")

    def get_absolute_url(self):
        return reverse('addplaylist')

    def __unicode__(self):
        return self.playlist_name


class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    artist_name = models.CharField(max_length=100, default="")
    artist_image = models.FileField()

    def __unicode__(self):
        return self.artist_name


class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=100, default="")
    artist_id = models.ForeignKey(Artist)

    def __unicode__(self):
        return self.album_name

    class Meta:
        unique_together = ['album_id', 'artist_id']


class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    album_id = models.ForeignKey(Album)
    artist_id = models.ForeignKey(Artist)
    song_name = models.CharField(max_length=100, default="")
    song_file = models.FileField(blank=True)
    song_image = models.FileField(blank=True)
    release_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.song_name)


class ListenCount(models.Model):
    listen_count_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User)
    song_id = models.ForeignKey(Song)
    count = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.song_id.song_id)

    class Meta:
        unique_together = ['user_id', 'song_id']


class PlayListSong(models.Model):
    playlist_song_id = models.AutoField(primary_key=True)
    playlist_id = models.ForeignKey(PlayList)
    song_id = models.ForeignKey(Song)

    def get_absolute_url(self):
        return reverse('addplaylist')

    def __str__(self):
        return str(self.playlist_song_id)
