import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(('Password must have at least one uppercase letter, '
                               'one lowercase letter and one number. The length should be '
                               'at least 8 characters.'),
                              code='Indalid'
                              )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Type your First Name')
        add_placeholder(self.fields['last_name'], 'Type your Last Name')
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password]
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must match'
        )
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'email': 'The email must be valid.'
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password2': 'Password and Password Confirm must match'
            })
