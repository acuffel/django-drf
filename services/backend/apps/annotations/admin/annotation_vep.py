from django.contrib import admin

from annotations.models import AnnotationVEP

@admin.register(AnnotationVEP)
class AnnotationVEPAdmin(admin.ModelAdmin):
    list_filter = ("annotation__id",)
