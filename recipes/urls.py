from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home_view, name="home"),
    path('recipes/<int:id>/', views.recipe_view, name="details"),
]
