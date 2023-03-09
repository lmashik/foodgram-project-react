from django.contrib import admin

from recipes.models import Tag, Ingredient, Recipe, IngredientAmount


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


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    """Отображение параметров Ingredient в административной части сервиса."""
    list_display = ('pk', 'name', 'author',)
    search_fields = ('name',)
    list_filter = ('name',)
    inlines = (
        IngredientAmountInline,
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)

