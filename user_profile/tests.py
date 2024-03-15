from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from group_chat.models import SavedPost, PostsModel, ChannelModel
from .models import UserProfile
from .forms import StatusForm


class UserProfileViewTest(TestCase):
    """
    Aotomated tests for user profile views
    """
    def setUp(self):
        """
        Set up the test environment by creating a test user,
        setting up the client, and logging in the user.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Log in the user
        self.client.login(username='testuser', password='testpassword')


    def test_user_profile_view(self):
        """
        Test the UserProfileView by making a GET request and checking the response.
        """

        # Get the URL for the UserProfileView
        url = reverse('user_profile')

        # Make a GET request to the user profile view
        response = self.client.get(url)
    
        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the user profile and other necessary data are in the context
        self.assertIn('user_profile', response.context)
        self.assertIn('Edit_profile_form', response.context)
        self.assertIn('profile_image_form', response.context)
        self.assertIn('status_form', response.context)
        self.assertIn('posts', response.context)

        # Check if the rendered template is correct
        self.assertTemplateUsed(response, 'user_profile/user_profile.html')


    def test_update_status(self):
        """
        Test updating user status by creating a StatusForm instance,
        saving it, and checking the updated status.
        """
        user_profile = UserProfile.objects.get(user=self.user)

        # Set up form data
        form_data = {'status': 'active'}

        # Create an instance of StatusForm with the user's profile as an instance
        form = StatusForm(form_data, instance=user_profile)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # If the form is valid, save it
        status = form.save()

        # check the status
        self.assertEqual(status.status, 'active')


    def test_remove_saved_post(self):
        """
        Test removing a saved post by creating a post,
        saving it, making a POST request, and checking the response.
        """
        # Create another user for testing
        another_user = User.objects.create_user(username='anotheruser', password='testpassword')
        channel = ChannelModel.objects.create(created_by=self.user, name='newchannel')

        # Create a post to be saved
        post_to_be_saved = PostsModel.objects.create(created_by=another_user, post='Test post content', post_channel=channel)

        # Save the post for the logged-in user
        SavedPost.objects.create(user=self.user, post=post_to_be_saved)

        # Get the URL for the remove_saved_post view
        url = reverse('remove_saved_post', args=[post_to_be_saved.id])

        # Make a POST request to remove the saved post
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains success message
        self.assertIn('status', response.json())
        self.assertEqual(response.json()['status'], 'Success')


    def test_get_all_users_profiles(self):
        """
        Test getting all users' profiles by making a GET request
        and checking the response status code and content.
        """
        # Get the URL for the get_all_users_profiles view
        url = reverse('get_all_user_profiles')

        # Make a GET request to get all users' profiles
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains user profiles
        self.assertTrue(response.json())


    def test_delete_user_account(self):
        """
        Test deleting the user account by making a POST request
        and checking the response status code and content.
        """
        # Get the URL for the delete_user_account view
        url = reverse('delete_account')

        # Make a POST request to delete the user account
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains success message
        self.assertIn('status', response.json())
        self.assertEqual(response.json()['status'], 'Success')
