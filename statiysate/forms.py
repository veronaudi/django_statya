from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(min_length=2, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'E-mail', 'id': 'id_email', 'class': 'form-control valid'}))
    message = forms.CharField(min_length=20, widget=forms.Textarea(attrs={'placeholder':'Сообщение', 'id': 'id_message', 'rows':9, 'cols':30, 'class': "form-control w-100"}))