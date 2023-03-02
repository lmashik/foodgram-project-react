from rest_framework import viewsets

from recipes.models import Tag
from api.serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
