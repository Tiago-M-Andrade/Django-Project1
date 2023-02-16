from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewBase.as_view(), name="home"),
    path('recipes/search/', views.search_view, name="search"),
    path('recipes/category/<int:category_id>/',
         views.category_view, name="category"),
    path('recipes/<int:id>/', views.recipe_view, name="details"),
]
