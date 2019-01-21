# Create your models here.

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        null=True
    )
    organisation_name = models.TextField(
        primary_key=True,
        blank=True,
        default="CIVIS"
    )
    organisation_logo = models.ImageField(
        upload_to='Organisation/Organisation Logo/%Y/%m/%d/', 
        null=True, 
        blank=True,
        verbose_name="Organisation Logo"
    )
    phone_number = models.CharField(
        blank=True, 
        max_length=10
    )

    def __str__(self):
        return self.organisation_name


class Header(models.Model):
    organisation_name = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL, 
        null=True
    )
    header = models.CharField(
       blank=True,
       max_length=200
    )
    class Meta:
        verbose_name_plural = 'Headers'

class Category(models.Model):
    organisation_name = models.ForeignKey(
        Profile, 
        on_delete=models.SET_NULL, 
        null=True
    )
    category = models.TextField(
       blank=True,
       max_length=200
    )
    class Meta:
        verbose_name_plural = 'Category'

class File(models.Model):
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    csv_file = models.FileField(
        upload_to='Organisation/CSV File/%Y/%m/%d/', 
        null=True, 
        blank=True
    )
    uploaded_date = models.DateTimeField(
        default=datetime.now, 
        null=True,
        blank=True
    )
    file_size = models.IntegerField(
        null=True,
        blank=True
    )
    file_name = models.TextField(
        blank = True
    )
    class Meta:
        verbose_name_plural = 'CSV File Meta Information'

    def __str__(self):
        return self.file_name
    