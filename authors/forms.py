from collections import defaultdict

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from base_templates.django_forms import (add_attr, add_placeholder,
                                         strong_password)
from recipes.models import Recipe


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


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['password'], 'Your password')

    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Portions', 'Portions'),
                    ('Unit', 'Unit'),
                    ('People', 'People'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutes', 'Minutes'),
                    ('Hours', 'Hours'),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cd = self.cleaned_data
        title = cd.get('title')
        description = cd.get('description')
        preparation_time = cd.get('preparation_time')
        servings = cd.get('servings')
        preparation_steps = cd.get('preparation_steps')

        if len(title) < 8:
            self._my_errors['title'].append(
                'The title must have at least 8 characters.')
        if len(description) < 19:
            self._my_errors['description'].append(
                'The description must have at least 20 characters.')
        try:
            if preparation_time < 0:
                self._my_errors['preparation_time'].append(
                    'Preparation time cannot be negative.')
        except BaseException:
            self._my_errors['preparation_time'].append(
                'Preparation time only accept whole numbers.')
        try:
            if servings < 0:
                self._my_errors['servings'].append(
                    'Servings cannot be negative.')
        except BaseException:
            self._my_errors['servings'].append(
                'Servings only accept whole numbers.')
        if len(preparation_steps) < 99:
            self._my_errors['preparation_steps'].append(
                'The preparation_steps must have at least 100 characters.')

        if self._my_errors:
            raise ValidationError(self._my_errors)
        return super_clean
