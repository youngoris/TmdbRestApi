from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Director, Actor, Genre, IMDBEntry, Movies

class IndexField(serializers.Field):
    def to_representation(self, value):
        movies_list = self.context.get('movies_list', [])
        for index, movie in enumerate(movies_list, start=1):
            if movie == value:
                return index
        return None

    # This field is read-only, so it does not need to support write operations.
    def to_internal_value(self, data):
        raise NotImplementedError("IndexField is read-only.")


# DirectorSerializer converts Director instances to and from JSON.
class DirectorSerializer(serializers.ModelSerializer):
    # Name field for the Director.
    name = serializers.CharField(max_length=255)
    # Nullable birth year.
    birth_year = serializers.IntegerField(allow_null=True, required=False)
    # Nullable death year.
    death_year = serializers.IntegerField(allow_null=True, required=False)

    # Custom validation to ensure death year is not before birth year.
    def validate(self, data):
        if data.get('death_year') and data.get('birth_year'):
            if data['death_year'] < data['birth_year']:
                raise serializers.ValidationError("Death year cannot be earlier than birth year.")
        return data

    class Meta:
        model = Director
        fields = '__all__'  # Include all fields in the serialized output.

    def create(self, validated_data):
        return Movies.objects.create(**validated_data)

# ActorSerializer for converting Actor instances.
class ActorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Actor
        fields = '__all__'  # Serialize all fields of the Actor model.

# GenreSerializer for converting Genre instances.
class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Genre
        fields = '__all__'  # Serialize all fields of the Genre model.

# IMDBEntrySerializer for converting IMDBEntry instances.
class IMDBEntrySerializer(serializers.ModelSerializer):
    imdb_id = serializers.CharField(max_length=255)

    # Custom validator to ensure the IMDB ID starts with "tt".
    def validate_imdb_id(self, value):
        if not value.startswith("tt"):
            raise serializers.ValidationError("IMDB ID must start with 'tt'.")
        return value

    class Meta:
        model = IMDBEntry
        fields = '__all__'  # Serialize all fields of the IMDBEntry model.

# MovieSerializer for converting Movies instances.
class MovieSerializer(serializers.ModelSerializer):

    index = IndexField(source='*', read_only=True)  # Adding custom index field to the serializer.

    title = serializers.CharField(max_length=255, allow_blank=False)
    release_date = serializers.DateField()
    vote_average = serializers.FloatField(min_value=0, max_value=10, allow_null=True)
    vote_count = serializers.IntegerField(min_value=0, allow_null=True)

    # Use SlugRelatedField to represent genres by their names.
    genres = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='name'  # Use Genre name for representation.
    )

    overview = serializers.CharField(allow_blank=True)

    # Use SlugRelatedField to represent casts by their names.
    casts = serializers.SlugRelatedField(
        many=True,
        queryset=Actor.objects.all(),
        slug_field='name'  # Use Actor name for representation.
    )

    # Use SlugRelatedField to represent directors by their names.
    directors = serializers.SlugRelatedField(
        many=True,
        queryset=Director.objects.all(),
        slug_field='name' # Use Director name for representation.
    )

    runtime = serializers.IntegerField(min_value=0, allow_null=False)
    adult = serializers.BooleanField()
    revenue = serializers.IntegerField(min_value=0, allow_null=True)
    budget = serializers.IntegerField(min_value=0, allow_null=True)

    # Primary key related field for IMDB ID.
    imdb_id = serializers.PrimaryKeyRelatedField(queryset=IMDBEntry.objects.all())


    def create(self, validated_data):
        # Pop and handle many-to-many relations data
        genres_data = validated_data.pop('genres', [])
        casts_data = validated_data.pop('casts', [])
        directors_data = validated_data.pop('directors', [])

        # Create the movie instance
        movie = Movies.objects.create(**validated_data)

        # Add genres, casts, and directors to the movie
        for genre_data in genres_data:
            genre, _ = Genre.objects.get_or_create(name=genre_data)
            movie.genres.add(genre)

        for actor_data in casts_data:
            actor, _ = Actor.objects.get_or_create(name=actor_data)
            movie.casts.add(actor)

        for director_data in directors_data:
            director, _ = Director.objects.get_or_create(name=director_data)
            movie.directors.add(director)

        return movie

    class Meta:
        model = Movies
        fields = '__all__'  # Serialize all fields of the Movies model.