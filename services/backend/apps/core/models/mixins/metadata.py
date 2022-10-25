from django.db import models


class MetadataMixin(models.Model):
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.metadata is None:
            self.metadata = {}
        super(MetadataMixin, self).save(*args, **kwargs)
