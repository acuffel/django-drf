from django.contrib import admin

from assemblies.models import Assembly


@admin.register(Assembly)
class AssemblyAdmin(admin.ModelAdmin):
    pass
