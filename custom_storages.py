"""
    contains custom storage backends for handling static and media files
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    """
    Custom storage backend for handling static files on Amazon S3.
    (Assuming you're using a custom Storage class that extends Storage)

    This storage backend sets the location for storing static files to the
    value specified in the Django settings (`STATICFILES_LOCATION`).

    Usage:
    - Set `STATICFILES_STORAGE` in your Django settings to
      'path.to.StaticStorage'.
    - Set `AWS_STORAGE_BUCKET_NAME` and other required AWS settings.

    Example:
    ```python
    AWS_STORAGE_BUCKET_NAME = 'your-s3-bucket'
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'path.to.StaticStorage'
    ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = settings.STATICFILES_LOCATION

    def get_accessed_time(self, name):
        """
        Return the last accessed time of the file.
        """
        raise NotImplementedError(
            "Method 'get_accessed_time' must be implemented in your StaticStorage class.")


class MediaStorage(S3Boto3Storage):
    """
    Custom storage backend for handling media files on Amazon S3.
    (Assuming you're using a custom Storage class that extends Storage)

    This storage backend sets the location for storing media files to the
    value specified in the Django settings (`MEDIAFILES_LOCATION`).

    Usage:
    - Set `DEFAULT_FILE_STORAGE` in your Django settings to
      'path.to.MediaStorage'.
    - Set `AWS_STORAGE_BUCKET_NAME` and other required AWS settings.

    Example:
    ```python
    AWS_STORAGE_BUCKET_NAME = 'your-s3-bucket'
    MEDIAFILES_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'path.to.MediaStorage'
    ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = settings.MEDIAFILES_LOCATION

    def get_accessed_time(self, name):
        """
        Return the last accessed time of the file.
        """
        raise NotImplementedError(
            "Method 'get_accessed_time' must be implemented in your MediaStorage class.")
