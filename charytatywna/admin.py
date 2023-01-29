from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Institution, Donation, FormData, FormDataResource

admin.site.register(Category)

@admin.register(FormData)
class FormDataAdmin(ImportExportModelAdmin):
    resource_class = FormDataResource

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'kategorie', 'description']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['institution', 'kategorie', 'quantity', 'user_email_name', 'is_taken']
    def user_email_name(self, obj):
        return obj.user.email_name()
    user_email_name.short_description = 'Użytkownik'


