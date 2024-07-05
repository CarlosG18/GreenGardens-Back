from django import forms
import re

class ContatoForm(forms.Form):
    """
        classe para o formulário de contato da landing page
    """

    nome = forms.CharField(
        max_length=100,
        label="Nome",
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': "Seu nome",
                'name': "nome",
            }
        ),
    )

    telefone = forms.CharField(
        max_length=16,
        label="Telefone",
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': "(xx) xxxxx-xxxx",
                'name': "telefone",
            }
        ),
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': "nome@email.com",
                'name': "email",
            }
        ),
    )

    mensagem = forms.CharField(
        max_length=100,
        label="Mensagem",
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': "O que você precisa?",
                'name': "mensagem",
                'rows': 10,
                'cols': 30,
            }
        ),
    )

def clean_nome(self):
    nome = self.cleaned_data.get('nome')
    nome_regex = r"^([a-zA-ZÀ-ÖØ-öø-ÿ]{2,}\s?)+$"

    if nome:
        if re.match(nome_regex, nome):
            return nome
        else:
            raise forms.ValidationError("formato de nome invalido!")

def clean_email(self):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    email = self.cleaned_data.get('email')

    if email:
        if re.match(email_regex, email):
            return email
        else:
            raise forms.ValidationError("formato de email invalido!")

def clean_telefone(self):
    tel_regex = r"^(?:\+\d{2}\s?)?(?:(?:\d{2}\s)?\d{4,5}-\d{4}|\d{4,5}-\d{4}|\d{4,5}\s\d{4}|\d{8,9})$"
    tel = self.cleaned_data.get('telefone')

    if tel:
        if re.match(tel_regex, tel):
            return tel
        else:
            raise forms.ValidationError("formato de telefone invalido!")