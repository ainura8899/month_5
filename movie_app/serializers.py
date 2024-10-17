from rest_framework import serializers
from movie_app.models import Movie, Director, Review
from movie_app.models import Category, SearchWord


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SearchWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchWord
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)  # Здесь будет 1 объект
    search_words = SearchWordSerializer(many=True)  # Здесь будет целый список
    category_name = serializers.SerializerMethodField()

    class Meta: #это класс который не меняется
        model = Movie
        fields = 'id comments category category_name search_words search_word_list title description director'.split()  # список из полей. Передаются id и title
        depth = 1 # обычно не используем, т.к. показывает все
        # fields = '__all__'
        # exclude = 'created text'.split()
        # category_name = serializer.SerializersMethodField()

    def get_category_name(self, movie):
        return movie.category.title if movie.category else None


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = 'id name movies_count'.split()  # список из полей. Передаются id и name

    def get_movies_count(self, director): # Метод get_movies_count фильтрует фильмы по текущему режиссёру
        return Movie.objects.filter(director=director).count() # и возвращает их количество с помощью .count().

class ReviewSerializer(serializers.ModelSerializer):
    movie_name = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = 'movie_name text '.split()
    def get_movie_name(self, review):
        return review.movie.title if review.movie else None