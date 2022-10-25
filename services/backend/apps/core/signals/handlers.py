from core.models import SiteCustomization
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Site)
def create_site_customization(sender, instance, created, **kwargs):
    if created:
        SiteCustomization.objects.create(site=instance)


@receiver(post_save, sender=Site)
def save_site_customization(sender, instance, **kwargs):
    instance.sitecustomization.save()
