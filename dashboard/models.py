from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from django.urls import reverse
from django_resized import ResizedImageField
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True)
    addressLine1 = models.CharField(null=True, blank=True, max_length=200)
    addressLine2 = models.CharField(null=True, blank=True, max_length=200)
    city = models.CharField(null=True, blank=True, max_length=100)
    state = models.CharField(null=True, blank=True, max_length=100)
    countries = CountryField(multiple=True)
    zipCode = models.CharField(null=True, blank=True, max_length=100)
    profileImage = ResizedImageField(
        size=[200, 200], quality=90, upload_to='profile_images')

    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.user.first_name, self.user.last_name, self.user.email)

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.slug = slugify('{} {} {}'.format(
            self.user.first_name, self.user.last_name, self.user.email))
        self.updated_at = timezone.localtime(timezone.now())
        super(Profile, self).save(*args, **kwargs)
