from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.shortcuts import render

from app.forms import AnimeForm
from app.models import User, Review, Anime


def home(req):
    return render(req, 'home.html', {'page_title': 'Home page'})


def newAnime(req):
    if req.method == 'POST':
        form = AnimeForm(req.POST)
        if form.is_valid():
            a = Anime(title=form.cleaned_data['title'], episodes=form.cleaned_data['episodes'], genre=form.cleaned_data['genre'])
            a.save()
            return redirect('app:new-anime')
        else:
            return render(req, 'newAnime.html', {'form': form})
    else:
        form = AnimeForm()
        return render(req, 'newAnime.html', {'form': form})


class GenreChartView(TemplateView):                  # broj anime po zanru chart
    template_name = 'genreChart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        anime = Anime.objects.all()
        query_set = []
        genre_set = set()
        for a in anime:
            genre_set.add(a.genre)
        for genre in genre_set:
            number_of_anime = 0
            for a in anime:
                if len(genre) > 0 and a.genre != genre:
                    continue
                number_of_anime += 1
            query_set.append({'genre': genre, 'number_of_anime': number_of_anime})
        query_set.sort(key=lambda l: l['number_of_anime'])
        context["qs"] = query_set
        context["char_type"] = self.request.GET.get('chartType', 'bar')
        return context


class AnimeReviewChartView(TemplateView):                  # reviews po animeu u vremenskom intervalu chart
    template_name = 'animeReviewChart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = self.request.GET.get('genre', '')
        date_from = self.request.GET.get('from', '')
        date_to = self.request.GET.get('to', '')
        anime = Anime.objects.all()
        reviews = Review.objects.all()
        query_set = []
        for a in anime:
            number_of_reviews = 0
            for review in reviews:
                if len(genre) > 0 and anime.genre != genre:
                    continue
                if len(date_from) > 0 and review.created_at < date_from:
                    continue
                if len(date_to) > 0 and review.created_at > date_to:
                    continue
                if review.anime == a.title:
                    number_of_reviews += 1
            query_set.append({'anime': a.title, 'number_of_reviews': number_of_reviews})
        query_set.sort(key=lambda l: l['number_of_reviews'])
        context["qs"] = query_set
        context["char_type"] = self.request.GET.get('chartType', 'bar')
        return context


class UserReviewChartView(TemplateView):                    # reviews po korisniku u vremenskom intervalu
    template_name = 'userReviewChart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_from = self.request.GET.get('from', '')
        date_to = self.request.GET.get('to', '')
        reviews = Review.objects.all()
        users = User.objects.all()
        query_set = []
        for user in users:
            number_of_reviews = 0
            for review in reviews:
                if len(user.email) > 0 and review.user != user.email:
                    continue
                if len(date_from) > 0 and review.created_at < date_from:
                    continue
                if len(date_to) > 0 and review.created_at > date_to:
                    continue
                number_of_reviews += 1
            if number_of_reviews > 0:
                query_set.append({'user': user.email, 'number_of_reviews': number_of_reviews})
        query_set.sort(key=lambda a: a['number_of_reviews'])
        context["qs"] = query_set
        context["char_type"] = self.request.GET.get('chartType', 'bar')
        return context
