from rest_framework import serializers
from movie_app.models import Movie, Director, Review
from movie_app.models import Category, SearchWord
from rest_framework.serializers import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
#
# class SearchWordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SearchWord
#         fields = '__all__'

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = 'id name movies_count'.split()  # список из полей. Передаются id и name

    def get_movies_count(self, director): # Метод get_movies_count фильтрует фильмы по текущему режиссёру
        return Movie.objects.filter(director=director).count() # и возвращает их количество с помощью .count().

class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=100)


class ReviewSerializer(serializers.ModelSerializer):
    movie_name = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = 'id movie_name text stars'.split()
    def get_movie_name(self, review):
        return review.movie.title if review.movie else None

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=2, max_length=100)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    def validate_text(self, value):
        if 'bad' in value:
            raise serializers.ValidationError('Bad text is not allowed')
        return value




class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    reviews = ReviewSerializer()
    average_rating =serializers.SerializerMethodField()
    category = CategorySerializer(many=False)  # Здесь будет 1 объект
    # search_words = SearchWordSerializer(many=True)  # Здесь будет целый список
    # category_name = serializers.SerializerMethodField()

    class Meta: #это класс который не меняется
        model = Movie
        fields = 'id title description category director reviews average_rating'.split()  # список из полей. Передаются id и title
        depth = 1 # обычно не используем, т.к. показывает все
        # fields = '__all__'
        # exclude = 'created text'.split()
        # category_name = serializer.SerializersMethodField()

    def get_average_rate(self, movies):
        reviews = movies.reviews.all()
        if reviews:
            average_rating = Review.objects.aggregate(Avg('stars')).get('stars__avg', 0)
            average_rating = round(average_rating, 1) if average_rating is not None else 0
            return Response({'average_rating': average_rating})
        return None

    # def create(self, validated_data):
    #     # Extract director data
    #     director_data = validated_data.pop('director')
    #
    #     # Either get an existing director or create a new one
    #     director, created = Director.objects.get_or_create(**director_data)
    #
    #     # Create the movie without the reviews field, which is read-only
    #     movie = Movie.objects.create(director=director, **validated_data)
    #
    #     return movie

    # def get_category_name(self, movie):
    #     return movie.category.title if movie.category else None
class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=5, max_length=255)
    description = serializers.CharField(min_length=10)
    #duration = serializers.IntegerField(min_value=1)
    #is_active = serializers.BooleanField()
    #view_count = serializers.IntegerField(min_value=0, max_value=100)
    category_id = serializers.IntegerField(min_value=1)
    director_id = serializers.IntegerField(min_value=1)
    #search_words = serializers.ListField(child=serializers.IntegerField(min_value=1))



    # def validate(self, attrs):
    #     category_id = attrs.get('category_id') #99
    #     try:
    #         Category.objects.get(id=category_id)
    #     except Category.DoesNotExist:
    #         raise ValidationError('Category does not exist')
    #     return attrs

    def validate_director_id(self, director_id): #99
        try:
             Director.objects.get(id=director_id)
        except Director.DoesNotExist:
             raise ValidationError('Director does not exist!')
        return director_id

    # def validate_search_words(self, search_words): # [1,2,99]
    #     search_words_db = SearchWord.objects.filter(id__in=search_words) # [1,2]
    #     if len(search_words_db) != len(search_words):
    #         raise ValidationError('Search words does not exist!')
    #     return search_words







