"""
Tests.py is for running automated tests
"""
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Conversation, Message, ImageModel


class MessagingTests(TestCase):
    """
    Test case for the InboxView.
    """

    def setUp(self):
        """
        Set up common test data.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.receiver = User.objects.create_user(username='testuser1',
                                                 password='testpassword1')
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

    def create_conversation_and_message(self):
        """
        Create a conversation and a message for testing.

        Returns:
        - Tuple: A tuple containing the created conversation and message.
        """
        # Create a conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user, self.receiver)

        # Create a message in the conversation
        message = Message.objects.create(
            sender=self.user,
            receiver=self.receiver,
            content='Test message',
            timestamp=datetime.now(),
            conversation=conversation
        )

        return conversation, message

    def test_get_inbox_view(self):
        """
        Test the GET request for the inbox view.
        """
        # Create a conversation and message
        conversation, message = self.create_conversation_and_message()

        # Call the InboxView
        response = self.client.get(reverse('inbox'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the rendered context contains the expected data
        self.assertEqual(len(response.context['messages']), 1)
        self.assertEqual(response.context['messages'][0], message)
        # unread message is created in signals.py when a new message created
        self.assertEqual(len(response.context['unread_messages']), 1)
        self.assertEqual(response.context['unread_messages'][0],
                         conversation.id)
        self.assertEqual(len(response.context['conversation_users']), 2)
        self.assertEqual(response.context['conversation_users'][0],
                         self.user)

        # Check if the rendered template is correct
        self.assertTemplateUsed(response, 'messaging/inbox.html')

    def test_get_message_list_view(self):
        """
        Test the GET request for the message list view.
        """
        # Create a conversation and message
        conversation, message = self.create_conversation_and_message()

        # Call the MessageListView for the conversation
        response = self.client.get(reverse(
            'message_list',
            args=[conversation.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the rendered context contains the expected data
        self.assertEqual(len(response.context['messages']), 1)
        self.assertEqual(response.context['messages'][0],
                         message)
        self.assertEqual(response.context['receiver'],
                         self.receiver)
        self.assertEqual(response.context['conversation_id'],
                         conversation.id)

        # Check if the rendered template is correct
        self.assertTemplateUsed(response, 'messaging/message-list.html')

    def test_post_message_list_view(self):
        """
        Test the POST request for the message list view.
        """
        # Create a conversation and message
        conversation, _ = self.create_conversation_and_message()

        # Create a message content for the POST request
        message_content = 'New test message'

        # Call the MessageListView with a POST request to send a new message
        response = self.client.post(reverse('message_list',
                                            args=[conversation.id]),
                                    {'post': message_content},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the message is created
        self.assertTrue(Message.objects.filter(
            content=message_content).exists())

    def test_delete_message_view(self):
        """
        Test the DELETE request for deleting a message.
        """
        # Create a conversation and message
        _, message = self.create_conversation_and_message()

        # Get the URL for the MessageDeleteView with the message_id parameter
        url = reverse('delete_message', args=[message.id])

        # Make a DELETE request to delete the message
        response = self.client.delete(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the message is deleted from the database
        with self.assertRaises(Message.DoesNotExist):
            Message.objects.get(id=message.id)

        # Check the JSON response for success
        expected_response = {'status': 'success',
                             'message': 'Message deleted'}
        self.assertEqual(response.json(), expected_response)

    def test_delete_conversation_view(self):
        """
        Test the DELETE request for deleting a conversation.
        """
        # Create a conversation and message
        conversation, _ = self.create_conversation_and_message()
        # Get the URL for the ConversationDeleteView with
        # the conversation_id parameter
        url = reverse('delete_conversation', args=[conversation.id])

        # Make a DELETE request to delete the conversation
        response = self.client.delete(url,
                                      HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the conversation is deleted from the database
        with self.assertRaises(Conversation.DoesNotExist):
            Conversation.objects.get(id=conversation.id)

        # Check the JSON response for success
        expected_response = {'status': 'success',
                             'message': 'Conversation deleted'}
        self.assertEqual(response.json(), expected_response)

    def test_upload_image_view(self):
        """
        Test the POST request for uploading an image.
        """
        # Create a sample image file for testing
        image_content = b'fake image content'
        image_file = SimpleUploadedFile("test_image.jpg",
                                        image_content,
                                        content_type='image/png')

        # Get the URL for the ImageUploadView
        url = reverse('image_upload')

        # Make a POST request to upload the image
        response = self.client.post(url, {'file': image_file},
                                    format='multipart',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if a new ImageModel instance is created
        self.assertTrue(ImageModel.objects.exists())

        # Check the JSON response for success
        new_image = ImageModel.objects.first()
        expected_response = {'status': 'Success',
                             'url': new_image.image.url}
        self.assertEqual(response.json(), expected_response)

    def test_upload_no_file_view(self):
        """
        Test the POST request for uploading an image without a file.
        """
        # Get the URL for the ImageUploadView
        url = reverse('image_upload')

        # Make a POST request without a file to simulate an error
        response = self.client.post(url,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)

        # Check the JSON response for an error message
        expected_response = {'status': 'Error',
                             'message': 'Image could not be uploaded'}
        self.assertEqual(response.json(), expected_response)
