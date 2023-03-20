from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    password = models.CharField(verbose_name='Password', max_length=150)
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=150,
        blank=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'password', 'first_name', 'last_name')

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('last_name',)

    def __str__(self):
        """Строковое представление объекта модели."""
        return f'{self.last_name} {self.first_name}'


class Subscription(models.Model):
    """Модель подписки."""
    subscriber = models.ForeignKey(
        User,
        verbose_name='Subscriber',
        related_name='subscribers',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        related_name='subscriptions',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = (
            models.UniqueConstraint(
                fields=('subscriber', 'author'),
                name='unique_subscription',
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('author')),
                name='no_self_subscription'
            ),
        )

    def __str__(self):
        """Строковое представление объекта модели."""
        return f'{self.subscriber} followed {self.author}'
