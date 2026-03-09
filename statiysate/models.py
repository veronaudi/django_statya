from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError("The Name field must be set")
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(name, password, **extra_fields)

class User(AbstractUser):
    username=None
    name=models.CharField(max_length=100, unique=True, verbose_name="Имя пользователя")

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()
    class Meta:
        verbose_name="Пользователь"
        verbose_name_plural= "Пользователи"

    def __str__(self):
        return self.name


class Article(models.Model):
    title=models.CharField(max_length=200, verbose_name="Название статьи")
    short_description=models.TextField(max_length=400, verbose_name="Краткое описание")
    text=models.TextField(verbose_name="Текст статьи")
    created_at=models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles", verbose_name="Автор", default=1)
    CATEGORY_CHOICES = [
        ("bit", "Быт"),
        ("studies", "Учеба"),
        ("work", "Работа"),
        ("food", "Еда"),
        ("emergency", "ЧП"),
        ("other", "Другое"),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other",verbose_name="Категория")

    class Meta:
        verbose_name="Статья"
        verbose_name_plural="Статьи"
        ordering=['-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Комментарий от {self.author_name}"
