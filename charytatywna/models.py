from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from import_export import resources, fields, widgets


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email jest obowiązkowy')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=30, verbose_name='Imię')
    last_name = models.CharField(max_length=60, verbose_name='Nazwisko')
    is_staff = models.BooleanField(default=False, verbose_name='SuperUser')
    is_active = models.BooleanField(default=True, verbose_name='Aktywny')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Data dołączenia')
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name}'

    def full_name(self):
        return f'{self.first_name} {self.last_name[0]}'

    def email_name(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=120, blank=False, verbose_name='Nazwa')

    def __str__(self):
        return self.name


class FormData(models.Model):
    categories = fields.Field(column_name='categories',
                              attribute='categories',
                              widget=widgets.ManyToManyWidget(Category, 'name'))


class FormDataResource(resources.ModelResource):
    categories = fields.Field(
        column_name='categories',
        attribute='categories',
        widget=widgets.ManyToManyWidget(Category, 'name')
    )
    class Meta:
        model = FormData

class Institution(models.Model):
    class OPTIONS(models.TextChoices):
        OPTION1 = 'fundacja', 'Fundacja'
        OPTION2 = 'organizacja pozarządowa', 'Organizacja pozarządowa'
        OPTION3 = 'zbiórka lokalna', 'Zbiórka lokalna'

    name = models.CharField(max_length=120, blank=False, verbose_name='Nazwa')
    description = models.TextField(verbose_name='Opis')
    type = models.CharField(max_length=26, choices=OPTIONS.choices,
                            default=OPTIONS.OPTION1, verbose_name='Rodzaj')
    category = models.ManyToManyField(Category, related_name='categories', verbose_name='Kategoria')

    def __str__(self):
        # categories_str = ', '.join([category.name[:8] for category in self.category.all()])
        # return f'{self.name} ({self.get_type_display()}) - {categories_str}.'
        return self.name

    @property
    def kategorie(self):
        return ', '.join([cat.name for cat in self.category.all()])



class DonationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(archived=False)


class Donation(models.Model):
    quantity = models.IntegerField(verbose_name='Ilość')
    categories = models.ManyToManyField(Category, verbose_name='Kategorie')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name='Instytucja')
    address = models.CharField(max_length=255, verbose_name='Ulica i numer')
    phone_number = models.CharField(max_length=20, verbose_name='Numer telefonu')
    city = models.CharField(max_length=255, verbose_name='Miasto')
    zip_code = models.CharField(max_length=10, verbose_name='Kod pocztowy')
    pick_up_date = models.DateField(verbose_name='Data odbioru')
    pick_up_time = models.TimeField(verbose_name='Godzina odbioru')
    pick_up_comment = models.TextField(blank=True, verbose_name='Informacja dla kuriera')
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Użytkownik')
    is_taken = models.BooleanField(default=False, verbose_name='Archiwizowane')

    # def clean(self):
    #     super().clean()
    #     phone_number = self.cleaned_data.get('phone_number')
    #     pattern = re.compile(r'^(\d{2,3})(\d{9,11})$')
    #     if not pattern.match(phone_number):
    #         raise ValidationError(
    #             "Numer telefonu jest niepoprawny, powinien zawierać kierunkowy 2-3 cyfry i 9-11 cyfr numeru.")

    def __str__(self):
        categories_str = ', '.join([category.name[:20] for category in self.categories.all()])
        return f'{self.institution.name} "{categories_str}" ({self.quantity}x).'

    @property
    def kategorie(self):
        return ', '.join([category.name for category in self.categories.all()])


    class Meta:
        ordering = ('pick_up_date', 'pick_up_time')
