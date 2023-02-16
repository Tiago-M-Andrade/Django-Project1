import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView

from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, ctx.get('recipes'), PER_PAGE)

        ctx.update({'recipes': page_obj,
                    'pages': pagination_range
                    })
        return ctx


def home_view(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/home.html',
                  context={'recipes': page_obj, 'pages': pagination_range})


def recipe_view(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html',
                  context={'recipe': recipe,
                           'is_detail_page': True})


def category_view(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(
        is_published=True, Category__id=category_id).order_by('-id'))

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/category.html',
                  context={
                    'recipes': page_obj,
                    'pages': pagination_range,
                    'title': f'{recipes[0].Category.name}'})  # noqa: E501


def search_view(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(Q(title__icontains=search_term) | Q(description__icontains=search_term)), is_published=True).order_by('-id')  # noqa: E501

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for "{ search_term }"',
        'search_term': search_term,
        'recipes': page_obj,
        'pages': pagination_range,
        'additional_url_query': f'&q={search_term}',
        })  # noqa: E501
