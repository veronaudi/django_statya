from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, User
from django.utils import timezone


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'mainn.html', {'articles': articles})


def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'article_detail.html', {'article': article})

def create_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        short_description = request.POST.get('short_description')
        text = request.POST.get('text')
        #author_id = request.POST.get('author_id')
        #user = User.objects.get(id=author_id)
        Article.objects.create(
            title=title,
            short_description=short_description,
            text=text,
            #user=user,
        )
        return redirect('home')
    users = User.objects.all()
    return render(request, 'create_article.html', {'users': users})


def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.short_description = request.POST.get('short_description')
        article.text = request.POST.get('text')
        article.save()
        return redirect('home')
    return render(request, 'edit_article.html', {'article': article})


def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    return redirect('home')