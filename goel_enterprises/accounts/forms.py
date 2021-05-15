from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class GuestForm(forms.Form):
    email = forms.EmailField()

class LoginForm(forms.Form):
    username = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class":"form-control",
                    }
                )
            )
    password = forms.CharField(
            widget=forms.PasswordInput(
                attrs={
                    "class":"form-control",
                    }
                )
            )

class RegisterForm(forms.Form):
    username = forms.CharField(
             widget=forms.TextInput(
                attrs={
                    "class":"form-control",
                    }
                )
             )
    password = forms.CharField(
            widget=forms.PasswordInput
            (
                attrs={
                    "class":"form-control",
                    }
                )
             )
    email = forms.EmailField(
            widget=forms.EmailInput(
                attrs={
                    "class":"form-control",

                    }
                )
            )
    password2 = forms.CharField(
            label = 'Confirm Password',
            widget= forms.PasswordInput
            (
                attrs={
                    "class":"form-control",
                    }
                )
            )
    def clean_username(self):
        username=self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if qs.exists():                                                                     # qs means query sets
            raise forms.ValidationError("Username is already taken")
        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():                                                                     # qs means query sets
            raise forms.ValidationError("email is already taken")
        return email


    def clean(self):
        data=self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password :
            raise forms.ValidationError("Passwords must match.")
        return data

