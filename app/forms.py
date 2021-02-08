from django.forms import ModelForm

from app.models import Review, Anime


class AnimeForm(ModelForm):

    class Meta:
        model = Anime
        fields = ['title', 'episodes', 'genre']


class ReviewForm(ModelForm):

    class Meta:
        model = Review
        fields = ['content']

