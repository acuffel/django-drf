from core.models import SiteCustomization
from modeltranslation.translator import TranslationOptions, translator


class SiteCustomizationTranslationOptions(TranslationOptions):
    fields = ("tagline", "description")


translator.register(SiteCustomization, SiteCustomizationTranslationOptions)
