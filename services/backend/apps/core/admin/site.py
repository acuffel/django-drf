from core.models import SiteCustomization
from django.contrib import admin
from django.contrib.sites.models import Site
from modeltranslation.admin import TranslationAdmin


class SiteAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)


class SiteCustomizationAdmin(TranslationAdmin):
    pass


admin.site.register(SiteCustomization, SiteCustomizationAdmin)
