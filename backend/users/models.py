from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_me


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Username',
        max_length=150,
        unique=True,
        validators=(
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Invalid username'
            ),
            validate_me,
        )
    )
    password = models.CharField(verbose_name='Password', max_length=128)
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=150,
        blank=True
    )

    REQUIRED_FIELDS = ('email', 'password', 'first_name', 'last_name')

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        """Строковое представление объекта модели."""
        return f'{self.last_name} {self.first_name}'


class Subscription(models.Model):
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
                name='Author cannot be self-followed',
            ),
        )


