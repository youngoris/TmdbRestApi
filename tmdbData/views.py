from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db.models import F, ExpressionWrapper, FloatField

# API view for fetching details of a single movie.
class MovieDetailView(APIView):
    def get(self, request, id):
        # Attempt to fetch a movie by tmdb_id, then by imdb_id if not found.
        try:
            movie = Movies.objects.get(tmdb_id=id)
        except Movies.DoesNotExist:
            try:
                movie = Movies.objects.get(imdb_id__imdb_id=id)
            except Movies.DoesNotExist:
                # Return 404 response if movie is not found.
                return Response(status=status.HTTP_404_NOT_FOUND)
        # Serialize the movie data.
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
class MovieCreateView(generics.CreateAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer

# API view for fetching movies by a specific actor.
class MoviesByActorView(APIView):
    def get(self, request, actor_name):
        actor_name_formatted = ' '.join(word.capitalize() for word in actor_name.split('_'))
        movies = Movies.objects.filter(casts__name=actor_name_formatted).order_by('-vote_average')
        movies_list = list(movies)
        serializer = MovieSerializer(movies_list, many=True, context={'movies_list': movies_list})
        return Response(serializer.data)

# API view for fetching movies by a specific genre.
class MoviesByGenreView(ListAPIView):
    serializer_class = MovieSerializer

    # Method to get a queryset of movies filtered by a specific genre.
    def get_queryset(self):
        # Replace underscores with spaces in the genre name and capitalize it.
        genre_name = self.kwargs['genre_name'].replace("_", " ").title()
        # Return a queryset of movies that match the genre, ordered by vote average.
        return Movies.objects.filter(genres__name__iexact=genre_name).order_by('-vote_average')
    
    # Overriding the list method to implement custom pagination and indexing.
    def list(self, request, *args, **kwargs):
        # Filter the queryset based on the view's filtering
        queryset = self.filter_queryset(self.get_queryset())
        # Paginate the filtered queryset.
        page = self.paginate_queryset(queryset)
        if page is not None:
            # Serialize the page of results.
            serializer = self.get_serializer(page, many=True)
            # Retrieve the current page number from the request query parameters.
            page_number = request.query_params.get(self.paginator.page_query_param, 1)
            try:
                # Convert page_number to an integer.
                page_number = int(page_number)
            except ValueError:
                # Default to the first page if conversion fails.
                page_number = 1
            # Calculate the start index for indexing movies on this page.
            start_index = 1 + (page_number - 1) * self.paginator.page_size
            # Add an index to each movie in the serialized data.
            for index, movie_data in enumerate(serializer.data, start=start_index):
                movie_data['index'] = index
            # Return the paginated response.
            return self.get_paginated_response(serializer.data)
        # Serialize the full queryset if pagination is not applied.
        serializer = self.get_serializer(queryset, many=True)
        # Add an index starting from 1 for non-paginated data.
        for index, movie_data in enumerate(serializer.data, start=1): 
            movie_data['index'] = index
        # Return the serialized data as a response.
        return Response(serializer.data)

# API view for fetching movies directed by a specific director.
class MoviesByDirectorView(APIView):
    def get(self, request, director_name):
        # Replace underscores and make sure queries are case-insensitive        
        director_name = director_name.replace("_", " ").title()
        # Query related movies directly based on the director's name
        movies = Movies.objects.filter(directors__name__iexact=director_name).order_by('-vote_average')
        # Serialize the movie data.
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
# API view for fetching top-rated movies.
class TopRatedMoviesView(APIView):
    def get(self, request, top_n):
        movies = Movies.objects.order_by('-vote_average')[:int(top_n)]
        movies_list = list(movies)
        serializer = MovieSerializer(movies_list, many=True, context={'movies_list': movies_list})
        return Response(serializer.data)

# API view for fetching movies with the best Return on Investment (ROI).
class BestROIView(APIView):
    def get(self, request, top_n):
        # Annotate movies with ROI calculation and fetch top N movies by ROI.
        movies = Movies.objects.annotate(
            roi=ExpressionWrapper(F('revenue') / F('budget'), output_field=FloatField())
        ).order_by('-roi')[:int(top_n)]
        movies_list = list(movies)
        serializer = MovieSerializer(movies_list, many=True, context={'movies_list': movies_list})
        return Response(serializer.data)
