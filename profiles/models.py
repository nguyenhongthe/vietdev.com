from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill
from simplemde.fields import SimpleMDEField
from unidecode import unidecode

from autoslug import AutoSlugField
from utils.common import generate_sha1


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(max_length=100, populate_from='name', editable=True, blank=True, db_index=True, unique=True)
    desc = SimpleMDEField(blank=True)
    desc_safe = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profiles:language', args=[self.slug])

    class Meta:
        ordering = ('-order', 'name')


class Technology(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(max_length=100, populate_from='name', editable=True, blank=True, db_index=True, unique=True)
    desc = SimpleMDEField(blank=True)
    desc_safe = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Technologies'
        ordering = ('-order', 'name')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profiles:tech', args=[self.slug])


class TechnologyMasteringLevel(models.Model):
    user = models.ForeignKey(User, related_name='+')
    technology = models.ForeignKey(Technology, related_name='+')
    self_rate = models.PositiveSmallIntegerField(default=0)
    year_exp = models.PositiveSmallIntegerField(default=1)

    ACTIVITY_CHOICES = (
        ('D', 'Daily'),
        ('W', 'Several days a week'),
        ('M', 'Several days a month'),
        ('S', 'Scattered'),
    )
    activity = models.CharField(choices=ACTIVITY_CHOICES, max_length=1, blank=True)
    involved_real_projects = models.BooleanField(default=False)

    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
        unique_together = ('user', 'technology')

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.technology.name, self.self_rate)


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(max_length=100, populate_from='name', editable=True, blank=True, db_index=True, unique=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-order', 'name')


class Software(models.Model):
    name = models.CharField(max_length=200, unique=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-order', 'name')


class Hardware(models.Model):
    name = models.CharField(max_length=200, unique=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-order', 'name')


def upload_avatar(instance, filename):
    extension = filename.split('.')[-1].lower()
    if extension not in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg']:
        extension = 'jpg'
    salt, h = generate_sha1(instance.id)
    return 'profile/{0}.{1}'.format(h[:10], extension)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    languages = models.ManyToManyField(ProgrammingLanguage, related_name='+', blank=True)

    location = models.ForeignKey(Location, blank=True, null=True)
    rate = models.DecimalField(default=1, max_digits=5, decimal_places=2, db_index=True)
    is_available = models.BooleanField(default=False, db_index=True)

    name = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    avatar = ProcessedImageField(upload_to=upload_avatar, blank=True,
                                 processors=[ResizeToFill(320, 320)],
                                 format='JPEG',
                                 options={'quality': 75})

    ENGLISH_CHOICES = (
        ('N', 'Native'),
        ('E', 'Excellent'),
        ('G', 'Good Reading, Good Speaking'),
        ('R', 'Good Reading, Average Speaking'),
        ('E', 'Good Enough for Works'),
    )
    english_level = models.CharField(choices=ENGLISH_CHOICES, blank=True, max_length=1, db_index=True)

    software = models.ManyToManyField(Software, related_name='+', blank=True)
    hardware = models.ManyToManyField(Hardware, related_name='+', blank=True)

    about = SimpleMDEField(blank=True)
    about_safe = models.TextField(blank=True)

    # social links
    homepage = models.URLField(max_length=200, blank=True)
    twitter = models.CharField(max_length=200, blank=True)
    github = models.CharField(max_length=200, blank=True)

    banned = models.BooleanField(default=False, db_index=True)
    banned_until = models.DateTimeField(null=True, blank=True)
    banned_reason = models.TextField(blank=True)

    total_points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # this profile is ready once has skills to be updated
    is_ready = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.user.username

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return settings.PERSON_DEFAULT

    def get_name(self):
        if self.name:
            return self.name
        return self.user.username

    def get_age(self):
        if self.birth_year:
            year = timezone.now().year
            age = round(year - self.birth_year)
            if 10 <= age <= 80:
                return age
        return ''

    def get_techs_list(self):
        return TechnologyMasteringLevel.objects.filter(user=self.user, removed=False).order_by('-year_exp')

    def has_techs(self):
        return TechnologyMasteringLevel.objects.filter(user=self.user, removed=False).exists()

    def get_homepage_name(self):
        if self.homepage:
            o = urlparse(self.homepage)
            return o.netloc
        return ''

    def show_refs(self):
        if self.homepage or self.github or self.twitter:
            return True
        return False

    def show_gears(self):
        if self.software.exists() or self.hardware.exists():
            return True
        return False

    def get_absolute_url(self):
        return reverse('profiles:profile', args=[self.user.username])

    def build_search_text(self):
        name_ = unidecode(self.name)
        name = self.name if self.name == name_ else '{} {}'.format(self.name, name_)
        txt = '{} {} {} {}'.format(self.user.username, name, self.user.email, self.job_title)
        return txt

    def build_search_autocomplete(self):
        name_ = unidecode(self.name)
        name = self.name if self.name == name_ else '{} {}'.format(self.name, name_)
        txt = '{} {}'.format(self.user.username, name)
        return txt

    class Meta:
        ordering = ('-created_at',)


class UserExperience(models.Model):
    user = models.ForeignKey(User, related_name='+')
    tech = models.ForeignKey(Technology, related_name='+')

    master_point = models.DecimalField(default=1, max_digits=5, decimal_places=2)
    started_since = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
