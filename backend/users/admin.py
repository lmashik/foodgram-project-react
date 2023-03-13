from django.contrib import admin

from users.models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    """Отображение параметров User в административной части сервиса."""
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name',)
    search_fields = ('first_name', 'last_name', 'email',)
    list_filter = ('username', 'email',)


class SubscriptionAdmin(admin.ModelAdmin):
    """Отображение параметров Subscription в административной части сервиса."""
    list_display = ('pk', 'author', 'subscriber',)


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
