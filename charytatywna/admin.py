from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Institution, Donation, FormData, FormDataResource

admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)

@admin.register(FormData)
class FormDataAdmin(ImportExportModelAdmin):
    resource_class = FormDataResource

