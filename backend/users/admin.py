from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    """Отображение параметров User в административной части сервиса."""
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name',)
    search_fields = ('first_name', 'last_name', 'email',)
    list_filter = ('username', 'email',)


admin.site.register(User, UserAdmin)
