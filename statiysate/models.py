from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя пользователя")
    email = models.EmailField(unique=True, verbose_name="Email")
    hashed_password = models.CharField(max_length=255, verbose_name="Хешированный пароль")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название статьи")
    short_description = models.TextField(max_length=500, verbose_name="Краткое описание")
    text = models.TextField(verbose_name="Текст статьи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles", verbose_name="Автор")
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
