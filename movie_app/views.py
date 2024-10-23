from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director, Movie, Review
from movie_app.serializers import MovieSerializer, DirectorSerializer, ReviewSerializer
from rest_framework import status
from django.db.models import Avg
from movie_app.serializers import MovieValidateSerializer, DirectorValidateSerializer, ReviewValidateSerializer


# Create your views here.

@api_view(http_method_names=['GET', 'POST'])
def movie_list_create_api_view(request):
    if request.method == 'GET':
        #print(request.query_params)
        #search = request.query_params.get('search', '')
        # step1: Collect movies (QuerySet) #собираем данные в виде списка Query
        movies = Movie.objects.all()
        #  movies = Movie.objects.select_related('category').prefetch_related('search_words','comments')

        # step2: Reformat movies to list of Dictionaries(JSON) # переводит в список из словарей
        data = MovieSerializer(instance=movies, many=True).data
        # step3: Return response as Json
        return Response(data=data)
    elif request.method == 'POST':
        # step0: Validation of data (Existance, Type, Extra) # Extra - каждое поле можно проверить самостоятельно
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                             data=serializer.errors)
        # step1: Receive data from request body
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        # duration = serializer.validated_data.get('duration')
        # is_active = serializer.validated_data.get('is_active')
        # view_count = serializer.validated_data.get('view_count')
        category_id = serializer.validated_data.get('category_id')
        director_id = serializer.validated_data.get('director_id')
        # search_words = serializer.validated_data.get('search_words')

        # step2: Create movie by received data
        movie = Movie.objects.create(
            title=title,
            description=description,
            # duration=duration,
            # is_active=is_active,
            # view_count=view_count,
            category_id=category_id, # Передаём экземпляр Category
            director_id=director_id # Передаём экземпляр Director
        )
        # movie.search_words.set(search_words)
        movie.save()

        # step3: Return response with data and status - Это в зав-ти от проекта
        return Response(status=status.HTTP_201_CREATED,
                        data={'movie_id': movie.id})


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    # step1: Collect movies (QuerySet)
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie is not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # step2: Reformat movies to list of Dictionaries(JSON) # переводит в список из словарей
        data = MovieSerializer(instance=movie, many=False).data

        # step3: Return response as JSON  # возвращает ответ в виде Json
        return Response(data=data) # передаем список в Response/data
    elif request.method == 'PUT':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data('description')
        # movie.duration = serializer.validated_data('duration')
        # movie.is_active = serializer.validated_data('is_active')
        # movie.view_count = serializer.validated_data('view_count')
        movie.category_id = serializer.validated_data('category_id')
        movie.director_id = serializer.validated_data('director_id')
        movie.save()
        return Response(data=MovieSerializer(movie).data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(http_method_names=['GET','POST'])
def director_list_api_view(request):
    if request.method == 'GET':
        # step1: Collect directors (QuerySet) #собираем данные в виде списка Query
        directors = Director.objects.all()
        #  directors = Director.objects.select_related('directors').prefetch_related('search_words','comments')

        # step2: Reformat directors to list of Dictionaries(JSON) # переводит в список из словарей
        data = DirectorSerializer(instance=directors, many=True).data
        # step3: Return response as Json
        return Response(data=data)
    elif request.method == 'POST':
        # step0: Validation of data (Existance, Type, Extra)
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        # step1: Receive data from request body
        name = serializer.validated_data.get('name')
        # movie_id = request.data.get('movie_id')


        # step2: Create director by received data
        directors = Director.objects.create(
            name=name,
            # movie_id=movie_id,
        )
       #movie.search_words.set(search_words)
        directors.save()

        # step3: Return response with data and status - Это в зав-ти от проекта
        return Response(status=status.HTTP_201_CREATED,
                        data={'directors_id': directors.id})


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    # step1: Collect directors (QuerySet)
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director is not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # step2: Reformat movies to list of Dictionaries(JSON)
        data = DirectorSerializer(instance=director, many=False).data

        # step3: Return response as JSON
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(data=DirectorSerializer(director).data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        # step1: Collect reviews (QuerySet) #собираем данные в виде списка Query
        reviews = Review.objects.all()
        #  reviews = Review.objects.select_related('review').prefetch_related('search_words','comments')

        # step2: Reformat reviews to list of Dictionaries(JSON) # переводит в список из словарей
        data = ReviewSerializer(instance=reviews, many=True).data
        # step3: Return response as Json
        return Response(data=data)

    elif request.method == 'POST':
        # step0: Validation of data (Existance, Type, Extra)
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        # step1: Receive data from request body
        text = serializer.validated_data.get('text')
        movie_id = serializer.validated_data.get('movie_id')
        stars = serializer.validated_data.get('stars')

        # step2: Create review by received data
        reviews = Review.objects.create(
            text=text,
            movie_id=movie_id,
            stars=stars
        )
        reviews.save()

        # step3: Return response with data and status - Это в зав-ти от проекта
        return Response(status=status.HTTP_201_CREATED,
                        data={'reviews_id': reviews.id})


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    serializer = ReviewValidateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)
    # step1: Collect reviews (QuerySet)
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review is not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # step2: Reformat reviews to list of Dictionaries(JSON)
        data = ReviewSerializer(instance=review, many=False).data

        # step3: Return response as JSON
        return Response(data=data)
    elif request.method == 'PUT':
        review.text = serializer.validated_data.get('text')
        review.movie_id = serializer.validated_data.get('movie_id')
        review.stars = serializer.validated_data.get('stars')
        review.save()
        return Response(data=ReviewSerializer(review).data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET'])
def review_movie_api_view(request):
    average_rating = Review.objects.aggregate(Avg('stars')).get('stars__avg', 0)
    average_rating = round(average_rating, 1) if average_rating is not None else 0
    return Response({'average_rating': average_rating})



