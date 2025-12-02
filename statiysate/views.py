from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponseNotFound
from .forms import ContactForm
from .models import Article, User
from django.utils import timezone
from .forms import CommentForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm



def article(request):
    articles=Article.objects.all()
    today=timezone.now().date()
    return render(request, 'mainn.html', {'articles': articles, 'today': today})

@login_required
def create_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        short_description=request.POST.get('short_description')
        text= request.POST.get('text')
        category = request.POST['category']
        #author_id = request.POST.get('author_id')
        user = request.user
        Article.objects.create(
            title=title,
            short_description=short_description,
            text=text,
            user=request.user,
            category=category
        )
        return redirect('home')
    users = User.objects.all()
    return render(request, 'create_article.html', {'categories': Article.CATEGORY_CHOICES})

@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        article.title=request.POST.get('title')
        article.short_description=request.POST.get('short_description')
        article.text=request.POST.get('text')
        article.category = request.POST.get('category')
        article.save()
        return redirect('home')
    return render(request, 'edit_article.html', {'article': article, 'categories': Article.CATEGORY_CHOICES})

@login_required
def delete_article(request, id):
    article=get_object_or_404(Article, id=id)
    article.delete()
    return redirect('home')

def about(request):
    return render(request, 'about.html')

def contactsnum(request):
    return render(request, 'contactsnum.html')


def contact(request):
    context = {}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            message=form.cleaned_data['message']
            send_message(name, email, message)
            context={'success': 1}
    else:
        form=ContactForm()
    context['form'] = form
    return render(request, 'contact.html', context=context)

def send_message(name, email, message):
    text=get_template('feedback.html')
    html=get_template('feedback.html')
    context={'name': name, 'email': email, 'message': message}
    subject='Обратрная связь от пользователя'
    from_email='from@example.com'
    text_content=text.render(context)
    html_content= html.render(context)

    msg=EmailMultiAlternatives(subject, text_content, from_email, ['manager@example.com'])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def article_list(request):
    """Показать все статьи, с возможностью поиска"""
    query = request.GET.get('q', '')
    if query:
        articles = Article.objects.filter(title__icontains=query)
    else:
        articles = Article.objects.all()
    return render(request, 'articles/list.html', {'articles': articles, 'query': query})


def article_by_category(request, category):
    """Фильтрация статей по категории"""
    valid_categories = [c[0] for c in Article.CATEGORY_CHOICES]
    if category not in valid_categories:
        return HttpResponseNotFound("<h2>Категория не найдена</h2>")

    articles = Article.objects.filter(category=category)
    return render(request, 'articles/list.html', {
        'articles': articles,
        'selected_category': category,
        'categories': Article.CATEGORY_CHOICES
    })

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all().order_by('-date')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('article_detail', id=article.id)
    else:
        form = CommentForm()

    return render(request, "article_detail.html", {
        "article": article,
        "comments": comments,
        "form": form,
    })

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматический вход после регистрации
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})
