from django.core.urlresolvers import reverse
from django.db import models
from simplemde.fields import SimpleMDEField
from autoslug.fields import AutoSlugField


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(max_length=50,
                         populate_from='title', editable=True, blank=True, db_index=True, unique=True)

    content = SimpleMDEField(blank=True)
    content_safe = models.TextField(blank=True)

    desc = models.CharField(max_length=300, blank=True)
    public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-updated_at',)

    def get_absolute_url(self):
        return reverse('pages:detail', args=[self.slug])
