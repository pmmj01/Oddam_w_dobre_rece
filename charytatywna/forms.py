from django import forms
from django.contrib.auth import get_user_model
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


# class DonationForm(forms.ModelForm):
#     class Meta:
#         model = Donation
#         fields = ['quantity', 'categories', 'institution', 'address', 'phone_number', 'city', 'zip_code',
#                   'pick_up_date', 'pick_up_time', 'pick_up_comment', 'user']
#
#     def clean_phone_number(self):
#         phone_number = self.cleaned_data.get('phone_number')
#         pattern = re.compile(r'^(\d{2,3})(\d{9,11})$')
#         if not pattern.match(phone_number):
#             raise forms.ValidationError(
#                 "Numer telefonu jest niepoprawny, powinien zawierać kierunkowy 2-3 cyfry i 9-11 cyfr numeru.")
#         return phone_number


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


# class DonationForm(forms.Form):
#     categories = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=[
#             ("clothes-to-use", "Clothes suitable for reuse"),
#             ("clothes-useless", "Clothes for disposal"),
#             ("toys", "Toys"),
#             ("books", "Books"),
#             ("other", "Other"),
#         ],
#     )


class DonationMultiForm(forms.ModelForm):
    QUANTITY_CHOICES = [(i, i) for i in range(1, 20)]
    quantity = forms.ChoiceField(choices=QUANTITY_CHOICES, widget=forms.Select(attrs={'class': 'quantity-select'}), required=True)
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    institution = forms.ModelChoiceField(queryset=Institution.objects.all(), widget=forms.Select, required=True)
    address = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    city = forms.CharField(required=True)
    zip_code = forms.CharField(required=True)
    pick_up_date = forms.CharField(widget=forms.SelectDateWidget(attrs={'placeholder': 'Data'}), required=True)
    pick_up_time = forms.TimeField(widget=forms.TextInput(attrs={'placeholder': 'Godzina (HH:MM)', 'pattern': '\d{2}:\d{2}'}), required=True)
    pick_up_comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Uwagi dla kuriera', 'rows': 5}), required=True)
    archived = forms.BooleanField(initial=False, required=True)

    def clean_pick_up_time(self):
        pick_up_time = self.cleaned_data.get('pick_up_time')
        if pick_up_time:
            pick_up_time_str = pick_up_time.strftime('%H:%M')
            if len(pick_up_time_str) > 5:
                self.add_error('pick_up_time', "Wprowadzony czas jest za długi (max 5 znaków)")
            if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', pick_up_time_str):
                self.add_error('pick_up_time', "Niepoprawny format godziny (HH:MM)")
            if int(pick_up_time.strftime('%M')) > 59:
                self.add_error('pick_up_time', "Minuta nie może być większa niż 59")
        return pick_up_time

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if zip_code:
            if len(zip_code) > 6:
                self.add_error('zip_code', "Wprowadzony kod pocztowy jest za długi (max 6 znaków)")
            if not re.match(r'^[0-9]{2}-[0-9]{3}$', zip_code):
                self.add_error('zip_code', "Niepoprawny format kodu pocztowego (XX-XXX)")
        return zip_code
    class Meta:
        model = Donation
        fields = ('quantity', 'categories', 'institution', 'address', 'phone_number', 'city', 'zip_code', 'pick_up_date', 'pick_up_time', 'pick_up_comment')

class UserEditForm(forms.Form):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']