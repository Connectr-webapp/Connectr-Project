"""
Forms module for the messaging app.

This module defines Django forms that are used for
user input and validation in the messaging app.
Currently, it includes a form for creating or updating messages.

Forms:
- MessageForm: Form for creating or updating messages.

For detailed information about each form and its usage,
refer to the individual docstrings
within the respective class definitions.

"""

from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    """
    Form for creating or updating messages.

    Attributes:
    - content (TextField): The content of the message.

    """
    class Meta:
        model = Message
        fields = ['content']
