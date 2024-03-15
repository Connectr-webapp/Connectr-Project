"""database Models for user profiles. """
from django.db import models
from django.contrib.auth import get_user_model

# pylint: disable=no-member

class UserProfile(models.Model):
    """Model for user profiles.

    Attributes:
    - user: One-to-One relationship with the User model.
    - username: User's username.
    - status: User's status (active or away).
    - profile_picture: User's profile picture.
    - last_viewed_channel_id: ID of the last channel viewed by the user.
    - phone: User's phone number.
    - mobile: User's mobile number.
    - location: User's location.
    - linkedin: User's LinkedIn profile.
    - github: User's GitHub profile.
    - website: User's personal website.
    - bio: User's biography.

    Methods:
    - __str__: Returns the string representation of the user profile.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('away', 'Away'),
    ]
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    username = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    last_viewed_channel_id = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    github = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True)


    def __str__(self):
        return self.user.username
