from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from group_chat.models import ChannelModel, PostsModel, CommentsModel


class GroupChatViewsTest(TestCase):
    """
    Test case for the group chat views.
    """

    def setUp(self):
        """
        Set up common test data.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword'
        )
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        self.channel = ChannelModel.objects.create(name='Test Channel')

    def test_channels_view(self):
        """
        Test the ChannelsView class methods.
        """
        url = reverse('view_channel', args=[self.channel.id])

        # Test the GET request for the channels view.
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'group_chat/home.html')

        # Test the POST request to add a user to the channel.
        another_user = get_user_model().objects.create_user(
            username='anotheruser', password='testpassword'
        )
        url_add_user = reverse(
            'add_user_to_channel', args=[self.channel.id, another_user.id]
        )
        response = self.client.post(
            url_add_user, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(another_user, self.channel.users.all())

    def test_posts_view(self):
        """
        Test the PostsView class methods.
        """
        url = reverse('channel_posts', args=[self.channel.id])

        # Test the GET request for the posts view.
        response = self.client.get(
            url, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'group_chat/posts.html')

        # Test the GET request for the posts view with pagination.
        for i in range(15):
            PostsModel.objects.create(
                created_by=self.user, post=f'Test post {i}',
                post_channel=self.channel
            )

        response = self.client.get(
            url, {'page': 2}, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'group_chat/paginated-posts.html')

        # Test the POST request to add a post to the posts view.
        post_data = {'post': 'Test post content'}
        response = self.client.post(
            url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PostsModel.objects.count(), 16)

        # Test the POST request to update an existing post in the posts view.
        existing_post = PostsModel.objects.create(
            created_by=self.user,
            post='Existing post',
            post_channel=self.channel
        )
        post_data = {'post': 'Updated post content'}
        url_with_post_id = reverse(
            'channel_posts', args=[self.channel.id, existing_post.id]
        )
        response = self.client.post(
            url_with_post_id, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)

    def test_comments_view(self):
        """
        Test the CommentsView class methods.
        """
        post = PostsModel.objects.create(
            created_by=self.user, post='Test post', post_channel=self.channel
        )
        url = reverse('post_comments', args=[post.id])

        # Test the GET request for the comments view.
        response = self.client.get(
            url, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'group_chat/comments.html')

        # Test the POST request to add a comment to the comments view.
        comment_data = {'post': 'Test comment content'}
        response = self.client.post(
            url, comment_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CommentsModel.objects.count(), 1)
