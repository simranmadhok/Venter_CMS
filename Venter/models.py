import os
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


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
    """
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

    def filename(self):
        return os.path.basename(self.csv_file.name) # pylint: disable = E1101

    class Meta:
        verbose_name_plural = 'CSV File Meta'
