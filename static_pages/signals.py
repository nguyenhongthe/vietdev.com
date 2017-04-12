import markdown2
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from . import models


@receiver(pre_save, sender=models.Page)
def make_safe_content(sender, instance, **kwargs):
    instance.content_safe = markdown2.markdown(instance.content,
                                               extras=["tables", "fenced-code-blocks", 'code-friendly'])

