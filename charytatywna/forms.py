from django import forms
from .models import *
import re


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Potwierdź hasło'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    # clean_password2 = lambda self: (
    #     self.cleaned_data.get('password') == self.cleaned_data.get('password2') or
    #     forms.ValidationError('Hasła nie są takie same')
    # )

    # def clean_password2(self):
    #     password = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')
    #     if password and password2 and password != password2:
    #         raise forms.ValidationError('Hasła nie są takie same')
    #     return password2

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")
        if password != password2:
            raise forms.ValidationError('Hasła muszą być takie same')
        try:
            CustomUser.objects.get(email=email)
            raise forms.ValidationError('Podany email już jest zarejestrowany')
        except CustomUser.DoesNotExist:
            pass


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['quantity', 'categories', 'institution', 'address', 'phone_number', 'city', 'zip_code',
                  'pick_up_date', 'pick_up_time', 'pick_up_comment', 'user']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        pattern = re.compile(r'^(\d{2,3})(\d{9,11})$')
        if not pattern.match(phone_number):
            raise forms.ValidationError(
                "Numer telefonu jest niepoprawny, powinien zawierać kierunkowy 2-3 cyfry i 9-11 cyfr numeru.")
        return phone_number


# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))
#
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.username = self.cleaned_data['email']
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         if commit:
#             user.save()
#         return user
#
#
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
#     # email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
#     # password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
