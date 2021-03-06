from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('season/<int:season_id>/', views.season_view, name='season'),
    path('season/<int:season_id>/stats', views.season_stats_view, name='season_stats'),
    path('team/<int:team_id>/', views.team_view, name='team'),
    path('driver/<int:driver_id>/', views.driver_view, name='driver'),
    path('league/<int:league_id>/', views.league_view, name='league'),
    path('division/<int:division_id>/', views.division_view, name='division'),
    path('race/<int:race_id>/', views.race_view, name='race'),
    path('track/<int:track_id>/', views.track_view, name='track'),
    path('laps/<int:result_id>', views.laps_view, name='laps'),
]
