from django import forms
from .models import Comment, User
from django.contrib.auth.forms import UserCreationForm


class ContactForm(forms.Form):
    name=forms.CharField(min_length=2, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'E-mail', 'id': 'id_email', 'class': 'form-control valid'}))
    message=forms.CharField(min_length=20, widget=forms.Textarea(attrs={'placeholder':'Сообщение', 'id': 'id_message', 'rows':9, 'cols':30, 'class': "form-control w-100"}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=["author_name", "text"]
        widgets={"author_name": forms.TextInput(attrs={"placeholder": "Ваше имя"}), "text": forms.Textarea(attrs={"placeholder": "Ваш комментарий"}),}

class RegisterForm(UserCreationForm):
    username = None  # <- ОТКЛЮЧАЕМ username !!!

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["name", "email"]  # именно твои поля!!!
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = None  # на всякий случай
        if commit:
            user.save()
        return user