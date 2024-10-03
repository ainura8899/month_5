from rest_framework import serializers
from movie_app.models import Movie, Director, Review

class MovieSerializer(serializers.ModelSerializer):

    class Meta: #это класс который не меняется
        model = Movie
        # fields = 'id title duration'.split()  # список из полей. Передаются id и title
        fields = '__all__'
        # exclude = 'created text'.split()
        # category_name = serializer.SerializersMethodField()


class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = 'id name'.split()  # список из полей. Передаются id и name

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text movie'.split()
