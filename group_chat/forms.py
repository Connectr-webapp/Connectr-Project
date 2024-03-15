from django import forms
from .models import PostsModel, CommentsModel


class PostsForm(forms.ModelForm):
    """
    This class is for the summernote editor form

    Parameters:
        super class: class that this class inherits from
    """
    class Meta:
        model = PostsModel
        fields = ['post', 'images']


class CommentsForm(forms.ModelForm):
    """
    This class is for the summernote editor form

    Parameters:
        super class: class that this class inherits from
    """
    class Meta:
        model = CommentsModel
        fields = ['post', 'images']
