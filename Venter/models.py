from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Organisation(models.Model):
    organisation_name = models.CharField(
        max_length=200,
        primary_key=True,
    )
    organisation_logo = models.ImageField(
        upload_to='Organisation/Organisation Logo/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name="Organisation Logo"
    )
    additional_details = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.organisation_name


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    organisation_name = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
    )
    profile_picture = models.ImageField(
        upload_to='Organisation/Employee Profile Picture/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name="Employee Profile picture"
    )
    phone_number = models.CharField(
        blank=True,
        max_length=10
    )

    def __str__(self):
        return self.user.username  # pylint: disable = E1101


class Header(models.Model):
    organisation_name = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )
    header = models.CharField(
        max_length=200
    )

    class Meta:
        verbose_name_plural = 'Headers'


class Category(models.Model):
    organisation_name = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )
    category = models.CharField(
        max_length=200
    )

    class Meta:
        verbose_name_plural = 'Category'


class File(models.Model):
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    csv_file = models.FileField(
        upload_to='Organisation/CSV File/%Y/%m/%d/',
    )
    uploaded_date = models.DateTimeField(
        default=datetime.now,
    )
    file_size = models.IntegerField()
    file_name = models.CharField(
        max_length=200
    )

    class Meta:
        verbose_name_plural = 'CSV File Meta Information'

    def __str__(self):
        return self.file_name
