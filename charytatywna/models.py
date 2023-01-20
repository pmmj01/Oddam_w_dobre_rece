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
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=60)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()


class Category(models.Model):
    name = models.CharField(max_length=120, blank=False)

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

    name = models.CharField(max_length=120, blank=False)
    description = models.TextField()
    type = models.CharField(max_length=26, choices=OPTIONS.choices,
                            default=OPTIONS.OPTION1)
    category = models.ManyToManyField(Category, related_name='institutions')

    def __str__(self):
        categories_str = ', '.join([category.name[:8] for category in self.category.all()])
        return f'{self.name} ({self.get_type_display()}) - {categories_str}'



class DonationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(archived=False)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(blank=True)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)

    # def clean(self):
    #     super().clean()
    #     phone_number = self.cleaned_data.get('phone_number')
    #     pattern = re.compile(r'^(\d{2,3})(\d{9,11})$')
    #     if not pattern.match(phone_number):
    #         raise ValidationError(
    #             "Numer telefonu jest niepoprawny, powinien zawierać kierunkowy 2-3 cyfry i 9-11 cyfr numeru.")

    def __str__(self):
        categories_str = ', '.join([category.name[:20] for category in self.categories.all()])
        return f'{self.institution} "{categories_str}" ({self.quantity}x)'