import json

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from sdufyStarter.models import *

from sdufyStarter.models import User, Music

from sdufyStarter.forms import *

from sdufyStarter.forms import UserImageForm

musics = Music.objects.all()
users = User.objects.all()


def home(request):
    profileExists = 'id' in request.session

    context = {
        'user': User.objects.all(),
        'profile': profileExists,
        'musics': Music.objects.all()
    }

    return render(request, 'sdufy/home.html', context)


def logout(request):
    del request.session['id']
    return redirect('index')


def search(request):
    search = request.GET.get('search')
    favInput = request.POST.get('favInput')
    context = {}
    print(search)
    user = User.objects.get(pk=request.session['id'])
    if search is not None:
        musics = Music.objects.filter(Q(artisticontains=search) | Q(titlecontains=search))
        profiles = User.objects.filter(Q(nameicontains=search) | Q(usernameicontains=search))
    else:
        musics = Music.objects.all()
        profiles = User.objects.all()
    favMusics_set = Favourite.objects.filter(user_id=user).values('music_id')
    if favInput:
        print(request.session['id'])
        music = Music.objects.get(pk=favInput)
        if Favourite.objects.filter(user_id=user,music_id=music).exists() == False:
            favourite = Favourite()
            favourite.user_id = user
            favourite.music_id = music
            favourite.save()
    playlists = Playlist.objects.all()

    if request.method == 'POST':
        print(request.POST)
        new_playlist = Playlist.objects.get(pk=request.POST.get('choice'))
        music = Music.objects.get(pk=favInput)
        playlistMusic = PlaylistMusic(playlist_id=new_playlist,music_id=music)
        playlistMusic.save()
    context['profiles'] = profiles
    context['search'] = search
    context['musics'] = musics
    context['playlists'] = playlists
    favMusics = []
    for favMusic in favMusics_set:
        favMusics.append(favMusic['music_id'])
    print(favMusics)
    context['favMusics'] = favMusics
    return render(request, 'sdufy/search.html',context)


def playlist2(request, id=None, music=None):
    if id is not None:
        playlistMusic = PlaylistMusic.objects.filter(playlist_id=id)
        playlistName = Playlist.objects.filter(id=id).first()
        playlist = Playlist.objects.get(pk=id)
        title = request.POST.get('title')
        coverPlaylist = request.POST.get('coverPlaylist')

        if title:
            playlist.title = title
        if coverPlaylist:
            playlist.coverPlaylist = coverPlaylist
        playlist.save()
        musicList = []
        for playlist in playlistMusic:
            musicList.append(Music.objects.filter(id=playlist.music_id_id))
        print(musicList, '---')


        return render(request, "sdufy/playlistMusic.html", {'musicList': musicList,
                                                            'playlistName': playlistName,
                                                            'mode': 'pause'})
    context = {}
    if request.method == 'POST':
        playlist = Playlist()
        title = request.POST.get('title_input')
        coverPlaylist = request.FILES.get('file_input')
        print(request.POST)
        print(request.FILES)
        if title:
            playlist.title = title
        if coverPlaylist:
            playlist.coverPlaylist = coverPlaylist
        playlist.save()
        return render(request, 'sdufy/search.html')

    # playlistUser = PlaylistUser.objects.filter(user_id=request.session['id'])
    # playlists = []
    # for playlist in playlistUser:
    #     playlists.append(Playlist.objects.filter(id=playlist.playlist_id_id))
    #
    # for playlist in playlists:
    #     print(playlist)
    #     for play in playlist:
    #         print(play.coverPlaylist.url, ' url')

    return render(request, 'sdufy/createPlaylist.html', context)



def playlist(request, id=None):
    if id is not None:
        playlistMusic = PlaylistMusic.objects.filter(playlist_id=id)
        playlistName = Playlist.objects.filter(id=id).first()
        musicList = []
        for playlist in playlistMusic:
            musicList.append(Music.objects.filter(id=playlist.music_id_id))
        print(musicList, '---')

        return render(request, "sdufy/playlistMusic.html", {'musicList': musicList,
                                                            'playlistName': playlistName})
    playlistUser = PlaylistUser.objects.filter(user_id=request.session['id'])
    playlists = []
    for playlist in playlistUser:
        playlists.append(Playlist.objects.filter(id=playlist.playlist_id_id))

    for playlist in playlists:
        print(playlist)
        for play in playlist:
            print(play.coverPlaylist.url, ' url')
    return render(request, 'sdufy/playlist.html', {'playlistUser': playlists})


def playMusic(request, id):
    print(PlaylistMusic.objects.filter(playlist_id=id))
    playlistMusic = PlaylistMusic.objects.filter(playlist_id=id)
    playlistName = Playlist.objects.filter(id=id).first()
    musicList = []
    for playlist in playlistMusic:
        musicList.append(Music.objects.filter(id=playlist.music_id_id))

    return render(request, "sdufy/playlistMusic.html", {'musicList': musicList,
                                                        'playlistName': playlistName,
                                                        'mode': 'play'})


def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(username, password)
        user = User.objects.filter(username=username, password=password).first()
        if username == "" or password == "":
            context = {
                'message': "Сначала заполните поля"
            }
            return render(request, 'sdufy/signin.html', context=context)
        if User.objects.filter(username=username, password=password).exists():
            request.session['id'] = user.id
            context = {
                'user': user
            }
            return render(request, 'sdufy/index.html', context)
        else:
            context = {
                'message': "Неверный логин или пароль"
            }
            return render(request, 'sdufy/signin.html', context=context)
    return render(request, 'sdufy/signin.html')


def logout(request):
    del request.session['id']
    return redirect('home')


def profile(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        'temp': 0,
        'user': user
    }
    return render(request, 'sdufy/profile.html', context=context)


def edit_profile(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        name = request.POST.get('name', None)
        user.name = name
        username = request.POST.get('username', None)
        user.username = username
        user.save()
        return redirect('profile')
    user = User.objects.get(id=request.session['id'])
    context = {
        'temp': 1,
        'user': user
    }
    return render(request, 'sdufy/profile.html', context=context)


def edit_password(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        'temp': 2,
        'user': user
    }
    if request.method == 'POST':
        oldpass = request.POST.get('oldpass')
        newpass1 = request.POST.get('newpass1')
        newpass2 = request.POST.get('newpass2')
        if oldpass != user.password:
            context['message'] = "It looks like you don't remember your password"
            return render(request, 'sdufy/profile.html', context=context)
        if newpass1 != newpass2:
            context['message'] = "Your passwords not same try again"
            return render(request, 'sdufy/profile.html', context=context)
        user = User.objects.get(id=request.session['id'])
        user.password = newpass1
        user.save()
    return render(request, 'sdufy/profile.html', context=context)


def admins(request):
    context = {
        "musics": musics,
        "users": users
    }
    return render(request, 'admin/admin.html', context)


def info(request):
    context = {
        "musics": musics,
        "users": users,
    }
    return render(request, 'admin/info.html', context)


def infoMusic(request):
    musics = Music.objects.all()
    users = User.objects.all()
    context = {
        "musics": musics,
        "users": users,
        'p_form': MusicImageForm()
    }
    return render(request, 'admin/musicPanel.html', context)


def ADD(request):
    musics = Music.objects.all()
    users = User.objects.all()
    if request.method == "POST":
        p_form = MusicImageForm(request.POST, request.FILES)
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        published = request.POST.get('published')
        duration = request.POST.get('duration')
        if p_form.is_valid():

            # p_form.save()
            music = Music(
                title=title,
                artist=artist,
                duration=duration,
                published=published,
                audio_file=p_form.cleaned_data['audio_file'],
                coverMusic=p_form.cleaned_data['coverMusic']
            )
            music.save()
            return redirect('musicPanel')
        else:
            return redirect('musicPanel')

    return redirect(request, 'admin/musicPanel.html')


def UPDATE(request,id):
    if request.method == "POST":
        music = Music.objects.get(pk=id)
        p_form = MusicImageForm(request.POST, request.FILES,instance=music)
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        published = request.POST.get('published')
        duration = request.POST.get('duration')
        if p_form.is_valid():
            music.title = title
            music.artist = artist
            music.pubihed = published
            music.duration = duration
            music.audio_file = p_form.cleaned_data['audio_file']
            music.coverMusic = p_form.cleaned_data['coverMusic']
            music.save()
            return redirect('musicPanel')
        else:
            return redirect('musicPanel')

    return redirect(request, 'admin/musicPanel.html')


def DELETE(request,id):
    musics = Music.objects.filter(id=id)
    musics.delete()

    context={
        'musics': musics
    }

    return redirect('musicPanel')


def info_user(request):
    users = User.objects.all()
    context = {
        "users": users,
        'u_form': UserImageForm()
    }
    return render(request, 'admin/userPanel.html', context)


def user_add(request):
    musics = Music.objects.all()
    users = User.objects.all()
    if request.method == "POST":
        u_form = UserImageForm(request.POST, request.FILES)
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if u_form.is_valid():
            users = User(
                name=name,
                username=username,
                password=password,
                type=1,
                avatarImg=u_form.cleaned_data['avatarImg'],
            )
            users.save()
            return redirect('userPanel')
        else:
            return redirect('userPanel')

    return redirect(request, 'admin/userPanel.html')

def user_update(request,id):
    if request.method == "POST":
        user = User.objects.get(pk=id)
        u_form = UserImageForm(request.POST, request.FILES, instance=user)
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        type = request.POST.get('type')
        if u_form.is_valid():
            user.name=name
            user.username=username
            user.password=password
            user.type=type
            user.avatarImg = u_form.cleaned_data['avatarImg']
            user.save()
            return redirect('userPanel')
        else:
            return redirect('userPanel')

    return redirect(request, 'admin/userPanel.html')

def user_delete(request,id):
    users = User.objects.filter(pk=id)
    users.delete()
    context={
        'user': users
    }
    return redirect('userPanel')





def notifications(request):
    user = User.objects.get(id=request.session['id'])

    id = request.session['id']
    userNo = Notification.objects.filter(pk=id)
    context = {
        'temp': 3,
        'user': user,
        'userNoti': userNo
    }
    return render(request, 'sdufy/profile.html', context=context)


def signUp(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        username = request.POST.get('username', None)
        password1 = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        avatarImg = request.POST.get('avatarImg', None)
        if name == "" or username == "" or password1 == "" or password2 == "":
            context = {
                'name': name,
                'username': username,
                'message': "Сначала заполните поля"
            }
            return render(request, 'sdufy/signup.html', context=context)
        if User.objects.filter(username=username):
            context = {
                'name': name,
                'message_name': "This username is already exist! Please try some other!"
            }
            return render(request, 'sdufy/signup.html', context=context)
        if password1 != password2:
            context = {
                'name': name,
                'username': username,
                'message': "Your passwords are not same, try again!",
            }
            return render(request, 'sdufy/signup.html', context=context)
        if len(password1) < 8:
            context = {
                'name': name,
                'username': username,
                'message': "Your password less than 8 characters"
            }
            return render(request, 'sdufy/signup.html', context=context)
        if not any(char.isdigit() for char in password1) or not any(char.isupper() for char in password1) or not any(
                char.islower() for char in password1):
            context = {
                'name': name,
                'username': username,
                'message': "Password should have at least one numeral, one uppercase letter and one lowercase letter"
            }
            return render(request, 'sdufy/signup.html', context=context)

        user = User.objects.create(name=name, username=username, password=password1, avatarImg=avatarImg)
        user.save()
        return redirect('signin')
    return render(request, 'sdufy/signup.html')


def favourite(request):
    return HttpResponse('favorite')


def search(request):
    search = request.GET.get('search')
    favInput = request.POST.get('favInput')
    context = {}
    print(search)
    user = User.objects.get(id=request.session['id'])
    if search is not None:
        musics = Music.objects.filter(Q(artist__icontains=search) | Q(title__contains=search))
        profiles = User.objects.filter(Q(name__icontains=search) | Q(username__icontains=search))
    else:
        musics = Music.objects.all()
        profiles = User.objects.all()
    favMusics = Favourite.objects.filter(user_id=user).values('music_id')
    if favInput:
        print(request.session['id'])
        music = Music.objects.get(pk=favInput)
        if Favourite.objects.filter(user_id=user, music_id=music).exists() == False:
            favourite = Favourite()
            favourite.user_id = user
            favourite.music_id = music
            favourite.save()
    context['profiles'] = profiles
    context['search'] = search
    context['musics'] = musics
    context['favMusics'] = favMusics
    playlistUser = PlaylistUser.objects.filter(user_id=request.session['id'])
    playlists = []
    for playlist in playlistUser:
        playlists.append(Playlist.objects.filter(id=playlist.playlist_id_id))

    context['playlistUser'] = playlists

    return render(request, 'sdufy/search.html', context)


def favourite(request):
    user = User.objects.get(pk=request.session['id'])
    musics = Favourite.objects.filter(user_id=user)
    print(musics)
    context = {
        'favMusics': musics, 'title': 'Favourite Musics'}
    return render(request, 'sdufy/favMusics.html', context)
