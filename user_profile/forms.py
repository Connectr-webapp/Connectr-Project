"""
Forms module for handling user profile-related forms.

This module includes forms for updating user status, profile picture, and editing
user profile information.

Classes:
- StatusForm: Form for updating the user status in the user profile.
- ProfileImageForm: Form for updating the user profile picture.
- EditProfileForm: Form for editing user profile information.
"""
from django import forms
from .models import UserProfile

class StatusForm(forms.ModelForm):
    """
    Form for updating the user status in the user profile.

    Attributes:
    - status: ChoiceField for selecting the user status.

    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('away', 'Away'),
    ]


    class Meta:
        """
        Meta class for the StatusForm.

        Attributes:
        - model: UserProfile model.
        - fields: List of fields to include in the form.

        """
        model = UserProfile
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['status'].label = 'Set Status'

class ProfileImageForm(forms.ModelForm):
    """
    Form for updating the user profile picture.

    Attributes:
    - profile_picture: ImageField for uploading the user profile picture.

    """
    class Meta:
        """
        Meta class for the ProfileImageForm.

        Attributes:
        - model: UserProfile model.
        - fields: List of fields to include in the form.

        """
        model = UserProfile
        fields = ['profile_picture']

class EditProfileForm(forms.ModelForm):
    """
    Form for editing user profile information.

    Attributes:
    - username: CharField for updating the username.
    - phone: CharField for updating the phone number.
    - mobile: CharField for updating the mobile number.
    - linkedin: CharField for updating the LinkedIn profile.
    - website: CharField for updating the website URL.
    - github: CharField for updating the GitHub profile.
    - location: CharField for updating the user's location.
    - bio: TextField for updating the user's biography.

    """
    class Meta:
        """
        Meta class for the EditProfileForm.

        Attributes:
        - model: UserProfile model.
        - fields: List of fields to include in the form.

        """
        model = UserProfile
        fields = ['username', 'phone', 'mobile', 'linkedin', 'website', 'github', 'location', 'bio']
       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize labels to remove the colon for all fields
        for field_name, field in self.fields.items():
            field.label_suffix = ''
            field.widget.attrs['placeholder'] = f'Enter your {field_name}'


class ContactForm(forms.Form):
    """
    A Django form for handling contact information.

    Fields:
    - subject (CharField): The subject of the contact message (max length: 100).
    - email (EmailField): The email address of the sender.
    - message (CharField): The message content (text area).

    Usage Example:
    form = ContactForm(request.POST)
    if form.is_valid():
        # Process the valid form data
    """
    subject = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)