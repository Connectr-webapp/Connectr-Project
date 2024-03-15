"""
views for the channels
"""
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from group_chat.models import ChannelModel, ChannelLastViewedModel
from messaging.models import UnreadMessage, Conversation


# pylint: disable=no-member
@method_decorator(login_required, name='dispatch')
class ChannelsView(View):
    """
    View class for displaying a list of channels.
    """

    template_name = 'group_chat/home.html'

    def get(self, request, channel_id=None, post_id=None):
        """
        Handle GET requests to display the list of channels.

        Returns:
            HttpResponse: Rendered template with channel information.
        """
        try:
            last_viewed_channel_id = None

            channels = ChannelModel.objects.all()
            if not channel_id:
                last_viewed_channel_id = request.user.userprofile.\
                                         last_viewed_channel_id

            # Create an empty dictionary to store user_status for each channel
            user_statuses = {}

            # Iterate over channels to get user_status for each
            for channel in channels:
                try:
                    if request.user in channel.users.all():
                        user_status, _ = ChannelLastViewedModel.objects.\
                                            get_or_create(
                                                user=request.user,
                                                channel=channel,
                                            )
                        user_statuses[channel.id] = user_status.last_visit
                except ChannelLastViewedModel.DoesNotExist:
                    # Handle the case where ChannelLastViewedModel
                    # does not exist for the user and channel
                    user_statuses[channel.id] = None

            unread_messages = self.get_unread_messages(request)

            context = {
                'channels': channels,
                'last_viewed_channel_id': last_viewed_channel_id,
                'user_statuses': user_statuses,
                'post_id': post_id,
                'channel_id': channel_id,
                'unread_messages': unread_messages
            }
            if request.session.pop('logged_in', False):
                context['logged_in'] = True


            return render(request, self.template_name, context)

        except Exception:
            return redirect('contact',
                             'Unexpected error retrieving homepage,\
                            Please contact us!!!')

    def get_unread_messages(self, request):
        """
        Get the latest unread message for each conversation.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            List[Message]: List of the latest unread messages
            in each conversation.
        """
        try:
            # Get the latest unread message for each conversation
            conversations = (
                UnreadMessage.objects
                .filter(conversation__participants=request.user)
                .values('conversation')
            )

            messages_by_conversation = []
            if conversations.exists():
                for conversation in conversations:
                    conv = Conversation.objects.get(
                            id=conversation['conversation']
                           )

                    # Retrieve the latest message in the conversation
                    latest_message = conv.messages.order_by(
                        '-timestamp'
                        ).first()

                    # Check if there is a latest message
                    # before adding it to the list
                    if latest_message and \
                       latest_message.receiver == request.user:
                        messages_by_conversation.append(latest_message)

            return messages_by_conversation

        except Exception:
            return None


@method_decorator(login_required, name='dispatch')
class AddUserToChannelView(View):
    """
    View class for adding a user to a channel.
    """
    def post(self, request, channel_id, user_id):
        # NOTE: The request parameter is not used in this method,
        # but it is kept for consistency.

        """
        Handle POST requests to add a user to a channel.

        Args:
            channel_id (int): The ID of the channel.
            user_id (int): The ID of the user.

        Returns:
            JsonResponse: JSON response indicating the status of the operation.
        """

        try:
            if not request.is_ajax():
                raise PermissionDenied
            channel = get_object_or_404(ChannelModel, id=channel_id)
            user = get_object_or_404(get_user_model(), id=user_id)

            # Add the user to the channel
            channel.users.add(user)

            return JsonResponse({
                'status': 'success',
                'message': f'{user.username} has been added to {channel.name}'
            })
        except ChannelModel.DoesNotExist:
            return JsonResponse({
                'status': 'Error',
                'message': 'Channel not found'
            }, status=404)
        except get_user_model().DoesNotExist:
            return JsonResponse({
                'status': 'Error',
                'message': 'User does not exist'
            }, status=404)
        except PermissionDenied:
            return render(request, '403.html')
        except Exception:
            return JsonResponse({'status': 500,
                                 'message': 'Unexpected error adding you to channel,\
                                 Please contact us!!!'},
                                status=500)



def get_all_channels(request):
    """
    Get a list of all channels with their names, IDs, and corresponding URLs.

    Returns:
    - JsonResponse: JSON response containing a list of
    dictionaries representing each channel.
      Each dictionary includes 'name', 'id', and 'url' keys.
      - 'status': 'success' if the operation is successful.
      - 'message': Additional details about the status.
    """
    try:
        if not request.is_ajax():
            raise PermissionDenied
        channels = ChannelModel.objects.all().values('name', 'id')

        # Create a list to store dictionaries representing each channel
        channel_list = []

        for channel in channels:
            # Get the URL for viewing the channel details
            url = reverse('view_channel', args=[channel['id']])

            # Add the 'url' key to the channel dictionary
            channel['url'] = url
            # Add the channel dictionary to the list
            channel_list.append(channel)

        return JsonResponse(list(channels), safe=False)
    except PermissionDenied:
        return render(request, '403.html')
    except Exception:
        return JsonResponse({'status': 500,
                                 'message': 'Unexpected error retrieving channels,\
                                 Please contact us!!!'},
                                status=500)
