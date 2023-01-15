from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe


def home_view(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html',
                  context={'recipes': recipes})


def recipe_view(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html',
                  context={'recipe': recipe,
                           'is_detail_page': True})


def category_view(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(
        is_published=True, Category__id=category_id).order_by('-id'))

    return render(request, 'recipes/pages/category.html',
                  context={'recipes': recipes, 'title': f'{recipes[0].Category.name}'})
