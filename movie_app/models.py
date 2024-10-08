from django.db import models
from django.db.models import Avg

# Create your models here.

class AbstractModel(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Category(AbstractModel):
    pass

class SearchWord(AbstractModel):
    pass

class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Movie(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    search_words = models.ManyToManyField(SearchWord, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    duration = models.DurationField()
    director = models.ForeignKey(Director, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    @property
    def search_word_list(self):
        return [i.title for i in self.search_words.all()]

STARS = (
    (1, '*'),
    (2, '**'),
    (3, '***'),
    (4, '****'),
    (5, '*****'),
)

class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name='comments')
    stars = models.IntegerField(choices=STARS, default=5)

    def __str__(self):
        return self.text

    def get_average_rating_for_all_movies():
        average_rating = Review.objects.aggregate(Avg('stars')).get('stars__avg', 0)
        return round(average_rating, 1) if average_rating is not None else 0

        average_rating = get_average_rating_for_all_movies()
        print(f'Средний рейтинг всех фильмов: {average_rating}')




