from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название статьи")
    short_description = models.TextField(max_length=500, verbose_name="Краткое описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
