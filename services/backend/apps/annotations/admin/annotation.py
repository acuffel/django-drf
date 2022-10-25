from django.contrib import admin

from annotations.models import Annotation

@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    pass
