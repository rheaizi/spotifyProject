"""sdufy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.template.context_processors import static
from django.urls import path

from sdufyStarter.views import *

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('playlist/', playlist, name='playlist'),
    path('createPlaylist/', playlist2, name='createPlaylist'),
    path('playlist/<id>/', playlist, name='playlist2'),
    path('playMusic/<id>/', playMusic, name='playMusic'),
    path('favourite/', favourite, name='favourite'),
    path('signin/', signIn, name='signin'),
    path('signup/', signUp, name='signup'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/edit/password/', edit_password, name='edit_password'),
    path('profile/notifications/', notifications, name='notifications'),
    path('admins/', admins, name='admin'),
    path('admins/music', infoMusic, name='musicPanel'),
    path('admins/user', info_user, name='userPanel'),
    path('admins/user/update/<str:id>', user_update, name='updateUser'),
    path('admins/user/add', user_add, name='addUser'),
    path('admins/delete/<str:id>', user_delete, name='deleteUser'),
    path('add', ADD, name='add'),
    path('update/<str:id>', UPDATE, name='update'),
    path('delete/<str:id>', DELETE, name='delete'),
    path('search/', search, name='search'),
    path('favourite/', favourite, name='favourite'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
