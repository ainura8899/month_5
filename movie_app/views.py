from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director, Movie, Review
from movie_app.serializers import MovieSerializer, DirectorSerializer, ReviewSerializer
from rest_framework import status

# Create your views here.

@api_view(http_method_names=['GET'])
def movie_list_api_view(request):
    # step1: Collect movies (QuerySet) #собираем данные в виде списка Query
    movies = Movie.objects.all()

    # step2: Reformat movies to list of Dictionaries(JSON) # переводит в список из словарей
    data = MovieSerializer(instance=movies, many=True).data


    # list_ = [] # пустой список
    # for movie in movies:
    #     list_.append({          # заполняем список
    #         'id': movie.id,
    #         'title': movie.title,
    #         'description': movie.description,
    #         'duration': movie.duration
    #     })

    # step3: Return response as JSON  # возвращает ответ в виде Json
    return Response(data=data)      # передаем список в Response/data

@api_view(http_method_names=['GET'])
def movie_detail_api_view(request, id):
    # step1: Collect movies (QuerySet)
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie is not found'},
                        tatus=status.HTTP_404_NOT_FOUND)

    # step2: Reformat movies to list of Dictionaries(JSON) # переводит в список из словарей
    data = MovieSerializer(instance=movie, many=False).data

    # step3: Return response as JSON  # возвращает ответ в виде Json
    return Response(data=data)      # передаем список в Response/data


@api_view(http_method_names=['GET'])
def director_list_api_view(request):
    # step1: Collect directors (QuerySet)
    directors = Director.objects.all()

    # step2: Reformat movies to list of Dictionaries(JSON)
    data = DirectorSerializer(instance=directors, many=True).data

    # step3: Return response as JSON
    return Response(data=data)

@api_view(http_method_names=['GET'])
def director_detail_api_view(request, id):
    # step1: Collect directors (QuerySet)
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director is not found'},
                        status=status.HTTP_404_NOT_FOUND)

    # step2: Reformat movies to list of Dictionaries(JSON)
    data = DirectorSerializer(instance=director, many=False).data

    # step3: Return response as JSON
    return Response(data=data)

@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    # step1: Collect directors (QuerySet)
    reviews = Review.objects.all()

    # step2: Reformat movies to list of Dictionaries(JSON)
    data = ReviewSerializer(instance=reviews, many=True).data

    # step3: Return response as JSON
    return Response(data=data)

@api_view(http_method_names=['GET'])
def review_detail_api_view(request, id):
    # step1: Collect directors (QuerySet)
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review is not found'},
                        status=status.HTTP_404_NOT_FOUND)

    # step2: Reformat movies to list of Dictionaries(JSON)
    data = ReviewSerializer(instance=review, many=False).data

    # step3: Return response as JSON
    return Response(data=data)