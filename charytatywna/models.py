from django.db import models
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=120, blank=False)


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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    archived = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        phone_number = self.cleaned_data.get('phone_number')
        pattern = re.compile(r'^(\d{2,3})(\d{9,11})$')
        if not pattern.match(phone_number):
            raise ValidationError(
                "Numer telefonu jest niepoprawny, powinien zawierać kierunkowy 2-3 cyfry i 9-11 cyfr numeru.")
