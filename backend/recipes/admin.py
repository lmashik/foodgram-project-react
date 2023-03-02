from django.contrib import admin

from recipes.models import Tag, Ingredient, Recipe


class TagAdmin(admin.ModelAdmin):
    """Отображение параметров Tag в административной части сервиса."""
    list_display = ('pk', 'name', 'colour', 'slug',)
    search_fields = ('name', 'colour',)
    list_filter = ('name', 'colour',)


class IngredientAdmin(admin.ModelAdmin):
    """Отображение параметров Ingredient в административной части сервиса."""
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    """Отображение параметров Ingredient в административной части сервиса."""
    list_display = ('pk', 'name', 'author',)
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)

