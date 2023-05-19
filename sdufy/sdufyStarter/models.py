from django.db import models

# Create your models here.

class UserType(models.TextChoices):
    USER = 1
    ADMIN = 2

class PlaylistType(models.TextChoices):
    USER = 1
    ADMIN = 2


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=UserType.choices, default=UserType.USER)
    avatarImg = models.ImageField(upload_to='user/')


class Music(models.Model):
    title = models.TextField()
    artist = models.TextField()
    published = models.IntegerField(max_length=255)
    duration = models.CharField(max_length=255)
    audio_file = models.FileField(blank=True, null=True)
    coverMusic =  models.ImageField(upload_to='music/')

    def __str__(self):
        return self.title

class Favourite(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.PROTECT)
    music_id = models.ForeignKey('Music', on_delete=models.PROTECT)

class Playlist(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=PlaylistType.choices)
    coverPlaylist = models.ImageField(upload_to='playlist/')

    def __str__(self):
        return self.title


class PlaylistUser(models.Model):
    playlist_id = models.ForeignKey('Playlist', on_delete=models.PROTECT)
    user_id = models.ForeignKey('User', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.playlist_id}"


class PlaylistMusic(models.Model):
    playlist_id = models.ForeignKey('Playlist', on_delete=models.PROTECT)
    music_id = models.ForeignKey('Music', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.music_id}"



class Notification(models.Model):
    music_id = models.ForeignKey('Music', on_delete=models.PROTECT)
    user_id = models.ForeignKey('User', on_delete=models.PROTECT)
    date = models.DateField(auto_now=True)