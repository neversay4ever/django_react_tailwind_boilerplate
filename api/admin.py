from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from djangoql.admin import DjangoQLSearchMixin
from django.core import serializers

# Register your models here.
from .models import APItest


class CustomModelAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name != "id"]
        self.search_fields = [
            field.name for field in model._meta.fields if field.name != "id"]
        super(CustomModelAdmin, self).__init__(model, admin_site)


@admin.register(APItest)
class APItestAdmin(CustomModelAdmin):
    pass
