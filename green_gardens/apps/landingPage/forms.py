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
        max_length=15,
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

    # função para validar o formato do email, permitindo apenas emails válidos
    def clean_email(self):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        email = self.cleaned_data.get('email')

        if email:
            if re.match(email_regex, email):
                return email
            else:
                raise forms.ValidationError("formato de email invalido!")

    # função para validar o formato de telefone, definido como validos os padrões referentes ao brasil
    def clean_telefone(self):
        tel_regex = r"^\(\d{2}\) \d{5}-\d{4}$"
        tel = self.cleaned_data.get('telefone')

        if tel:
            if re.match(tel_regex, tel):
                return tel
            else:
                raise forms.ValidationError("formato de telefone invalido!")