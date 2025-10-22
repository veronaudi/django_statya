from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template

from .forms import ContactForm
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

def about(request):
    return render(request, 'about.html')

def contactsnum(request):
    return render(request, 'contactsnum.html')


def contact(request):
    context = {}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_message(name, email, message)
            context = {'success': 1}
    else:
        form = ContactForm()
    context['form'] = form
    return render(request, 'contact.html', context=context)

def send_message(name, email, message):
    text = get_template('feedback.html')
    html = get_template('feedback.html')
    context = {'name': name, 'email': email, 'message': message}
    subject = 'Обратрная связь от пользователя'
    from_email = 'from@example.com'
    text_content = text.render(context)
    html_content = html.render(context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, ['manager@example.com'])
    msg.attach_alternative(html_content, "text/html")
    msg.send()