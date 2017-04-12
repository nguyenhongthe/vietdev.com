from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import markdown2

from . import models
from . import content_processors


@receiver(post_save, sender=User)
def create_new_profile(sender, instance, **kwargs):
    models.Profile.objects.get_or_create(user=instance)


@receiver(pre_save, sender=models.Profile)
def profile_pre_save(sender, instance, **kwargs):

    # make HTML from markdown
    if instance.about:
        content = markdown2.markdown(instance.about, extras=["tables", "fenced-code-blocks", 'code-friendly'])
        instance.about_safe = content_processors.cleanup_html(content)


@receiver(post_save, sender=models.Profile)
def profile_post_save(sender, instance, created, **kwargs):

    # calc total points
    total = 0
    list_ = models.TechnologyMasteringLevel.objects.filter(user=instance.user, removed=False)
    for x in list_:
        if x.self_rate >= 90:
            total += x.self_rate * 4
        elif x.self_rate >= 75:
            total += x.self_rate * 3
        elif x.self_rate >= 50:
            total += x.self_rate * 2
        else:
            total += x.self_rate

    models.Profile.objects.filter(pk=instance.id).update(total_points=total)

    # is profile ready?
    if not instance.is_ready:
        if instance.has_techs():
            models.Profile.objects.filter(pk=instance.id).update(is_ready=True)


@receiver(pre_save, sender=models.ProgrammingLanguage)
def language_pre_save(sender, instance, **kwargs):

    # make HTML from markdown
    if instance.desc:
        content = markdown2.markdown(instance.desc, extras=["tables", "fenced-code-blocks", 'code-friendly'])
        instance.desc_safe = content_processors.cleanup_html(content)


@receiver(pre_save, sender=models.Technology)
def technology_pre_save(sender, instance, **kwargs):

    # make HTML from markdown
    if instance.desc:
        content = markdown2.markdown(instance.desc, extras=["tables", "fenced-code-blocks", 'code-friendly'])
        instance.desc_safe = content_processors.cleanup_html(content)
