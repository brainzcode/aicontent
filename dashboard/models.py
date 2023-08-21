from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from django.urls import reverse
from django_resized import ResizedImageField
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from .country import COUNTRIES


import os


class Profile(models.Model):
    SUBSCRIPTION_OPTIONS = [
        ('free', 'free'),
        ('starter', 'starter'),
        ('advance', 'advance')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addressLine1 = models.CharField(null=True, blank=True, max_length=200)
    addressLine2 = models.CharField(null=True, blank=True, max_length=200)
    city = models.CharField(null=True, blank=True, max_length=100)
    state = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(
        max_length=100, choices=COUNTRIES, default='Select Country')
    zipCode = models.CharField(null=True, blank=True, max_length=100)
    phone_number = models.CharField(max_length=50, blank=True)
    profileImage = ResizedImageField(
        size=[200, 200], quality=90, upload_to='profile_images')

    # Subscription Helpers
    monthlyCount = models.CharField(null=True, blank=True, max_length=100)
    subscribed = models.BooleanField(default=False)
    subscriptionType = models.CharField(
        choices=SUBSCRIPTION_OPTIONS, default='free', max_length=100)
    subscriptionReference = models.CharField(
        null=True, blank=True, max_length=500)

    # Utility Variables
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.user.first_name, self.user.last_name, self.user.email)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.slug = slugify('{} {} {}'.format(
            self.user.first_name, self.user.last_name, self.user.email))
        self.updated_at = timezone.localtime(timezone.now())
        super(Profile, self).save(*args, **kwargs)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    blogIdea = models.CharField(null=True, blank=True, max_length=200)
    keywords = models.CharField(null=True, blank=True, max_length=400)
    audience = models.CharField(null=True, blank=True, max_length=100)
    wordCount = models.CharField(null=True, blank=True, max_length=100)

    # Related Field
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # Utility Variables
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.title, self.uniqueId)

    # def get_absolute_url(self):
    #     return reverse('profile-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.slug = slugify('{} {}'.format(self.title, self.uniqueId))
        self.updated_at = timezone.localtime(timezone.now())
        super(Blog, self).save(*args, **kwargs)


class BlogSection(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    wordCount = models.CharField(null=True, blank=True, max_length=200)

    # Utility Variables
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.title, self.uniqueId)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.slug = slugify('{} {}'.format(self.title, self.uniqueId))
        self.updated_at = timezone.localtime(timezone.now())
        # Count Words
        if self.body:
            wordsCounted = len(self.body.split(' '))
            self.wordCount = str(wordsCounted)
        super(BlogSection, self).save(*args, **kwargs)
