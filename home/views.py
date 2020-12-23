from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import View
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import UserForm
from django.views import generic
from django.shortcuts import render
from .models import Artist, Song, PlayList, PlayListSong, ListenCount
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from popularity_reco import popular_song
from user_collab import song_pred
from item_collab import get_songs


@login_required(login_url="/login/")
def songs(request):
    choice = request.POST.getlist("checks", "")
    choice = map(int, choice)
    choices = Song.objects.filter(artist_id__in=choice)
    return render(request, 'home/songs.html', {'choices': choices})


@login_required(login_url="/login/")
def player(request):
    plays = request.POST.get("choose", "")
    u = map(int, plays)
    i = u[0]
    try:
        plays = Song.objects.get(song_id=plays)
        listen_count_obj = ListenCount.objects.filter(user_id=request.user.id)
        print(listen_count_obj)
        print(i)
        has = False
        for obj in listen_count_obj:
            if i == obj.song_id.song_id:
                obj.count += 1
                obj.save()
                has = True
        if not has:
            ListenCount.objects.create(
                user_id=request.user,
                song_id=plays,
                count=1
            )

        d = song_pred(request.user.id)
        w = []
        for n in d:
            w.append(n)
        l = map(int, w)
        # print(l)
        blah = list(Song.objects.filter(pk__in=l))
        blah.sort(key=lambda h: l.index(h.pk))
        # print(blah)
        recc = blah
        # recc = Song.objects.filter(song_id__in=l) #yesma
        # print(recc)
        e = get_songs(request.user.id, i)
        t = []
        for m in e:
            t.append(m)
        p = map(int, t)
        # print(p)
        # p=pks_list = [10, 2, 1]
        themes = list(Song.objects.filter(pk__in=p))
        themes.sort(key=lambda g: p.index(g.pk))
        # print(themes)
        it = themes

        # it = Song.objects.filter(song_id__in=p)'it': it                  #yesma

    except:
        raise Exception("Exception here")
    return render(request, 'home/player.html', {'play': plays, 'recc': recc, 'it': it})


class SelectView(LoginRequiredMixin, generic.ListView):
    template_name = 'home/select.html'

    def get_queryset(self):
        return Artist.objects.order_by("?")


class LoginSelectView(LoginRequiredMixin, generic.ListView):
    template_name = 'home/loginselect.html'

    def get(self, request, *args, **kwargs):
        b = popular_song()
        print(b)
        s = []
        for y in b:
            s.append(y)
        c = map(int, s)
        print(c)
        bad = list(Song.objects.filter(pk__in=c))
        bad.sort(key=lambda x: c.index(x.pk))
        return render(request, self.template_name, {'bad': bad})


def home(request):
    return render(request, 'home.html')


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'home/addplaylist.html'

    def get_queryset(self):
        return PlayList.objects.all()


class DetailView(LoginRequiredMixin, generic.ListView):
    template_name = "home/playlist_detail.html"

    def get_queryset(self):
        return PlayListSong.objects.all()


class PlaylistCreate(LoginRequiredMixin, CreateView):
    model = PlayList
    fields = ['playlist_id', 'playlist_name']

    # def get_absolute_url(self):
    #     return self.get_success_url()

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user_id = self.request.user
        obj.save()
        return HttpResponseRedirect('/addplaylist/')


class PlaylistDelete(LoginRequiredMixin, DeleteView):
    model = PlayList
    success_url = reverse_lazy('addplaylist')


class PlaylistsongCreate(LoginRequiredMixin, CreateView):
    model = PlayListSong
    fields = ['playlist_song_id', 'song_id', 'playlist_id']


class PlaylistsongDelete(LoginRequiredMixin, DeleteView):
    model = PlayListSong
    success_url = reverse_lazy('addplaylist')


class UserFormView(View):
    form_class = UserForm
    template_name = 'signup.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('select')

        return render(request, self.template_name, {'form': form})
