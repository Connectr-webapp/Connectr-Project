from django.db import models
from django.contrib.auth import get_user_model

# pylint: disable=no-member


class ChannelModel(models.Model):
    """
    Model for each individual channel.

    Attributes:
    - created_by: User who created the channel.
    - created_date: Date and time when the channel was created.
    - is_private: Boolean indicating whether
    the channel is private or not.
    - name: Name of the channel.
    - users: Many-to-Many relationship with users
    who are members of the channel.

    Methods:
    - latest_post: Returns the latest post in the channel.
    """
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        null=True, related_name='%(class)s_created'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=True)
    name = models.CharField(max_length=254, default='')
    users = models.ManyToManyField(get_user_model(),
                                   related_name='channels')

    @property
    def latest_post(self):
        """
        - latest_post: Returns the latest post in the channel.
        """
        return self.posts_created.latest('created_date')


class ChannelLastViewedModel(models.Model):
    """
    Model for tracking the last viewed time of a channel by a user.

    Attributes:
    - user: User who viewed the channel.
    - channel: Channel that was viewed.
    - last_visit: Date and time of the last visit.

    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    channel = models.ForeignKey(ChannelModel, on_delete=models.CASCADE)
    last_visit = models.DateTimeField(auto_now=True)


class ImageModel(models.Model):
    """
    Model for storing images.

    Attributes:
    - image: ImageField for uploading images.

    """
    image = models.ImageField(upload_to='images/')


class EmojiModel(models.Model):
    """
    Model for storing emojis.

    Attributes:
    - emoji_colon_name: Text field for storing the
    colon representation of the emoji.
    - users_who_incremented: Many-to-Many relationship
    with users who incremented the emoji.

    Methods:
    - get_incremented_users: Returns the users who incremented the emoji.

    """
    emoji_colon_name = models.TextField(unique=False)
    users_who_incremented = models.ManyToManyField(
        get_user_model(),
        related_name='%(class)s_incremented',
        blank=True
    )

    def get_incremented_users(self):
        """
        - get_incremented_users: Returns the users who incremented the emoji.
        """
        return self.users_who_incremented.all()


class PostsModel(models.Model):
    """
    Model for each individual post in a channel.

    Attributes:
    - created_by: User who created the post.
    - created_date: Date and time when the post was created.
    - name: Name of the post.
    - images: TextField for storing image URLs.
    - emojis: Many-to-Many relationship with emojis in the post.
    - post: Text field for the content of the post.
    - post_channel: Foreign key to the channel where the post was created.

    Methods:
    - get_image_urls: Returns a list of image URLs in the post.
    - latest_comment: Returns the latest comment on the post.

    """
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='%(class)s_created'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=254, default='')
    images = models.TextField(blank=True, default="")
    emojis = models.ManyToManyField(EmojiModel)
    post = models.TextField()
    post_channel = models.ForeignKey(
        ChannelModel, on_delete=models.CASCADE,
        related_name='posts_created'
    )

    def get_image_urls(self):
        """
        - get_image_urls: Returns a list of image URLs in the post.
        """
        return [url.strip() for url in self.images.split(',') if url.strip()]

    @property
    def latest_comment(self):
        """
        - latest_comment: Returns the latest comment on the post.
        """
        return self.comments_created.latest('created_date')


class CommentsModel(models.Model):
    """
    Model for comments on each individual post.

    Attributes:
    - created_by: User who created the comment.
    - created_date: Date and time when the comment was created.
    - name: Name of the comment.
    - emojis: Many-to-Many relationship with emojis in the comment.
    - images: TextField for storing image URLs in the comment.
    - post: Text field for the content of the comment.
    - comment_post: Foreign key to the post where the comment was created.

    Methods:
    - get_image_urls: Returns a list of image URLs in the comment.

    """
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='%(class)s_created'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=254, default='')
    emojis = models.ManyToManyField(EmojiModel)
    images = models.TextField(blank=True, default="")
    post = models.TextField()
    comment_post = models.ForeignKey(
        PostsModel, on_delete=models.CASCADE,
        related_name='comments_created'
    )

    def get_image_urls(self):
        """
        - get_image_urls: Returns a list of image URLs.
        """
        return [url.strip() for url in self.images.split(',') if url.strip()]


class SavedPost(models.Model):
    """
    Model for storing saved posts by users.

    Attributes:
    - user: A foreign key to the user who saved the post.
    - post: A foreign key to the post that is saved.
    - created_at: Date and time when the saved post entry was created.

    Meta:
    - unique_together: Ensures that the combination of user and post is unique,
    preventing duplicate entries for the same saved post.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(PostsModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        - unique_together: Ensures that the combination
        of user and post is unique,
        preventing duplicate entries for the same saved post.
        """
        unique_together = ['user', 'post']


class UnseenPost(models.Model):
    channel = models.ForeignKey(ChannelModel, on_delete=models.CASCADE)
    unseen_users = models.ManyToManyField(get_user_model(),
                                          related_name='unseen_posts')

    def __str__(self):
        return f"{self.channel.name} - {self.last_seen_post_id}"
