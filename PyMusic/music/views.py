from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from music.models import Album, Song
from .forms import UserForm, SongForm


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGES_FILE_TYPES = ['png', 'jpg', 'jpeg']

class IndexView(generic.ListView):
	template_name = 'music/index.html'
	context_object_name = 'albums'

	def get_queryset(self):
		return Album.objects.all()

class DetailView(generic.DetailView):
	model = Album
	template_name = 'music/songs_detail.html'

class AlbumCreate(CreateView):
	model = Album
	fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumUpdate(UpdateView):
	model = Album
	fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumDelete(DeleteView):
	model = Album
	success_url = reverse_lazy('music:index')


class UserFormView(View):
	form_class = UserForm
	template_name = 'music/registration_form.html'
	
	#login
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})

	#register
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False)

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			#returns user object when credientials are correct
			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('music:index')

		return render(request, self.template_name, {'form':form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
	form = UserForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			albums = Album.objects.filter(user=request.user)
			return render(request, 'music/index.html', {'album':album})
	context = {
		'form':form
	}
	return render(request, 'music/register.html', context)


def logout_user(request):
	logout(request)
	form = UserForm(request.POST or None)
	context = {
		"form":form,
	}
	return render(request, 'music/login.html', context)


def create_song(request, album_id):
	form = SongForm(request.POST or None, request.FILES or None)
	album = get_object_or_404(Album, pk=album_id)
	if form.is_valid():
		album_songs = album.song_set.all()
		for s in album_songs:
			if s.song_title == form.cleaned_data.get("song_title"):
				context = {
					'album':album,
					'form':form,
					'error_message':'You have already added the song'	
				}
				return render(request, 'music/create_song.html', context)
		song = form.save(commit = False)
		song.album = album
		song.audio_file = request.FILES['audio_file']
		file_type = song.audio_file.url.split('.')[-1]
		file_type = file_type.lower()
		if file_type not in AUDIO_FILE_TYPES:
			context={
				'album': album,
				'form': form,
				'error_message': 'Audio file must be WAV, MP3, OGG'
			}
			return render(request, 'music/create_song.html', context)

		song.save()
		return render(request, 'music/detail.html', {'album':album})
	context = {
		'album':album,
		'form':form
	}
	return render(request, "music/create_song.html", context)
