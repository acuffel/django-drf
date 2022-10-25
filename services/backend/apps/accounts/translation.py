from modeltranslation.translator import TranslationOptions, translator

from accounts.models import User


class UserTranslationOptions(TranslationOptions):
    pass


translator.register(User, UserTranslationOptions)
