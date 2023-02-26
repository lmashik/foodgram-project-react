from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User

from .serializers import UserSerializer


def sign_up():
    pass


def get_jwt_toke():
    pass


class UserViewSet(viewsets.ModelViewSet):
    """Представление для пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsSuperUserOrAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'delete', 'patch',)

    @action(
        methods=('get', 'patch',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        """Обработка url users/me/."""
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                user, partial=True, data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )


