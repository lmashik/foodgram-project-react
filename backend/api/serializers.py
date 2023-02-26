from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)
