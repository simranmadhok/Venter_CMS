import os
from datetime import datetime, date

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


def get_file_upload_path(instance, filename):
    """
    Returns a custom MEDIA path for files uploaded by a user
    Eg: /MEDIA/CSV Files/xyz/user1/2019-02-06/file1.csv
    """
    return os.path.join(
        f'CSV Files/{instance.uploaded_by.profile.organisation_name}/{instance.uploaded_by.profile.user.username}/{instance.uploaded_date.date()}/{filename}')

def get_organisation_logo_path(instance, filename):
    """
    Returns a custom MEDIA path for organisation logo uploaded by staff member
    Eg: /MEDIA/Organisation Logo/xyz/2019-02-06/image1.png
    """
    return os.path.join(
        f'Organisation Logo/{instance.organisation_name}/{date.today()}/{filename}')


def get_user_profile_picture_path(instance, filename):
    """
    Returns a custom MEDIA path for profile picture uploaded by user
    Eg: /MEDIA/User Profile Picture/xyz/user1/2019-02-06/image2.png
    """
    return os.path.join(
        f'User Profile Picture/{instance.organisation_name}/{instance.user.username}/{date.today()}/{filename}')

class Organisation(models.Model):
    """
    An organisation that the user belongs to.
    Eg: user_1 belongs to xyz organisation

    # Create an organisation
    >>> organisation_1 = Organisation.objects.create(organisation_name="xyz", organisation_logo="image1.png")
    >>> organisation_2 = Organisation.objects.create(organisation_name="abc", additional_details="Mumbai based company")
    """
    organisation_name = models.CharField(
        max_length=200,
        primary_key=True,
    )
    organisation_logo = models.ImageField(
        upload_to=get_organisation_logo_path,
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
    """
    A Profile associated with an existing user.
    Eg: organisation name and phone number are some profile details associated with user_1

    # Create a user profile
    >>> prof_1 = Profile.objects.create(user=user_1, organisation_name="abc", profile_picture="image2.png")
    >>> prof_2 = Profile.objects.create(user=user_2, organisation_name="abc", phone_number="9999999999")
    """
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
        upload_to=get_user_profile_picture_path,
        null=True,
        blank=True,
        # verbose_name="Employee Profile picture"
    )
    phone_number = models.CharField(
        blank=True,
        max_length=10,
        validators=[RegexValidator(regex='^[6-9]\d{9}$', message='Please enter a valid phone number.')]
    )

    def __str__(self):
        return self.user.username  # pylint: disable = E1101


class Header(models.Model):
    """
    A Header list associated with each organisation.
    Eg: Organisation xyz may contain headers in the csv file such as- user_id, title etc

    # Create a header instance
    >>> Header.objects.create(organisation_name="xyz", header="user_id")
    """
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
    """
    A Category list associated with each organisation.
    Eg: Organisation xyz may contain categories in the csv file such as- hawkers, garbage etc

    # Create a category instance
    >>> Category.objects.create(organisation_name="xyz", category="hawkers")
    """
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
    """
    A File uploaded by the logged-in user.
    Eg: user_1 may upload a .csv file on 12/12/12

    # Create a file instance
    >>> File.objects.create(uploaded_by=user_1, csv_file="file1.csv", uploaded_date = "Jan. 29, 2019, 7:59 p.m.")

    Meta class------
        1) declares a plural name for the 'File' object
    """
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    csv_file = models.FileField(
        upload_to=get_file_upload_path
    )
    uploaded_date = models.DateTimeField(
        default=datetime.now,
    )

    def filename(self):
        """
        Returns the name of the csv file uploaded.
        Usage: dashboard_user.html template
        """
        return os.path.basename(self.csv_file.name)  # pylint: disable = E1101

    class Meta:
        verbose_name_plural = 'CSV File Meta'
