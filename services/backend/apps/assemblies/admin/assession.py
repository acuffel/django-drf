from django.contrib import admin

from assemblies.models import Assession


@admin.register(Assession)
class AssessionAdmin(admin.ModelAdmin):
    pass
