from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    name=models.CharField(max_length=100, unique=True, verbose_name="Имя пользователя")

    USERNAME_FIELD = 'name'  # теперь логин — это name
    REQUIRED_FIELDS = ['email']  # email обязателен
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
        ("tech", "Технологии"),
        ("sport", "Спорт"),
        ("news", "Новости"),
        ("art", "Искусство"),
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
