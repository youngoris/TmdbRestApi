"""
URL configuration for TmdbRestApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tmdbData.views import (MovieDetailView, MovieCreateView, MoviesByActorView, MoviesByGenreView,  
                            MoviesByDirectorView, TopRatedMoviesView, BestROIView)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Admin site URL. Provides the interface for site administrators.
    path("admin/", admin.site.urls),

    # URL pattern for movie detail view. 
    path('movies/<int:id>/', MovieDetailView.as_view(), name='movie-detail'),
    
    path('movies/create/', MovieCreateView.as_view(), name='create-movie'),

    # URL pattern for movies by actor view. 
    path('movies/actor/<str:actor_name>/', MoviesByActorView.as_view(), name='movies-by-actor'),

    # URL pattern for movies by genre view. 
    path('movies/genre/<str:genre_name>/', MoviesByGenreView.as_view(), name='movies-by-genre'),

    # URL pattern for top-rated movies view. 
    path('movies/top-rated/<int:top_n>/', TopRatedMoviesView.as_view(), name='top-rated-movies'),

    # URL pattern for best return on investment (ROI) movies view. 
    path('movies/best-roi/<int:top_n>/', BestROIView.as_view(), name='best-roi-movies'),

    # URL pattern for movies by director view. 
    path('movies/director/<str:director_name>/', MoviesByDirectorView.as_view(), name='movies-by-director'),

    # Static files URL pattern. Used during development to serve static files.
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Static files URL pattern. Used during development to serve static files.