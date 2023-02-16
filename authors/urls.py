from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/recipe/create/', views.dashboard_recipe_create_view,
         name='dashboard_recipe_create'),
    path('dashboard/recipe/<int:id>/delete/', views.dashboard_recipe_delete_view,  # noqa
         name='dashboard_recipe_delete_view'),
    path('dashboard/recipe/<int:id>/edit/', views.dashboard_recipe_edit_view,
         name='dashboard_recipe_edit'),
]
