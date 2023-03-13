from django.contrib import admin
from recipes.models import (Favorites, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


class TagAdmin(admin.ModelAdmin):
    """Отображение параметров Tag в административной части сервиса."""
    list_display = ('pk', 'name', 'colour', 'slug',)
    search_fields = ('name', 'colour',)
    list_filter = ('name', 'colour',)


class IngredientAdmin(admin.ModelAdmin):
    """Отображение параметров Ingredient в административной части сервиса."""
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name__istartswith',)
    list_filter = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    """Отображение параметров Ingredient в административной части сервиса."""
    list_display = ('pk', 'name', 'author', 'additions_to_favorites',)
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    inlines = (
        RecipeIngredientInline,
    )

    def additions_to_favorites(self, obj):
        return Favorites.objects.filter(recipe=obj).count()


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'recipe',)


class FavoritesAdmin(admin.ModelAdmin):
    """Отображение параметров Favorites в администратичной части сервиса."""
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)


class ShoppingCartAdmin(admin.ModelAdmin):
    """Отображение параметров ShoppingCart в администратичной части сервиса."""
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
