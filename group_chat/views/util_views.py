from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.views.generic import DeleteView
from django.core.exceptions import PermissionDenied
from django.apps import apps
from group_chat.models import PostsModel, ImageModel, SavedPost


# pylint: disable=no-member

class ImageUploadView(View):
    """
    View class for handling image uploads.
    """
    def post(self, request):
        """
        Handle POST requests to upload an image.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: JSON response indicating
            the status of the image upload.
        """
        try:
            if not request.is_ajax():
                raise PermissionDenied
            allowed_file_types = ['image/jpeg', 'image/png',
                                  'image/gif', 'image/bmp',
                                  'image/webp', 'image/tiff']
            if request.FILES.get('file'):
                image_file = request.FILES['file']
                if image_file.content_type not in allowed_file_types:
                    return JsonResponse({'status': 'Error',
                                         'message': 'File type not allowed'},
                                        status=400)

                # Create a new ImageModel instance
                new_image = ImageModel.objects.create(image=image_file)

                # Return the URL
                return JsonResponse(
                    {'status': 'Success',
                     'url': new_image.image.url}
                )

            return JsonResponse({'status': 'Error',
                                 'message': 'Image could not be uploaded'})
        except PermissionDenied:
            return render(request, '403.html')
        except Exception:
            return JsonResponse({'status': 500,
                                 'message': 'Unexpected error\
                                 occurred while uploading image, \
                                 Please contact us!!!'},
                                status=500)


class AddOrUpdateEmojiView(View):
    """
    View class for adding or updating an emoji in a
    post or comments model instance.
    """
    def post(self, request, instance_id, *args, **kwargs):
        """
        Handle POST requests to add or update an
        emoji in a post or comments model instance.

        Args:
            request (HttpRequest): The HTTP request object.
            instance_id (int): The ID of the model instance.

        Returns:
            JsonResponse: JSON response indicating the status of the operation.
        """
        try:
            if not request.is_ajax():
                raise PermissionDenied
            user = request.user
            emoji_colon_name = request.POST.get('emoji_colon_name')

            # Get the model class based on the URL parameter
            model_name = self.kwargs['model']
            model = apps.get_model(app_label='group_chat',
                                   model_name=model_name)

            obj = get_object_or_404(model, pk=instance_id)

            # If it exists, increment the count and add the user
            instance, created = obj.emojis.get_or_create(
                emoji_colon_name=emoji_colon_name,
                defaults={'emoji_colon_name': emoji_colon_name}
            )

            if created:
                # If a new instance is created, add the user
                instance.users_who_incremented.add(user)
                return JsonResponse({'status': 'added'})

            # Check if the EmojiModel exists
            if request.user in instance.users_who_incremented.all():
                instance.users_who_incremented.remove(user)
                # Check if there are no more users and
                # remove the instance if true
                if instance.users_who_incremented.count() == 0:
                    obj.emojis.remove(instance)
                    return JsonResponse({'status': 'removed'})
                return JsonResponse({'status': 'decremented'})

            # If it exists, increment the count and add the user
            instance.users_who_incremented.add(user)
            return JsonResponse({'status': 'incremented'})
        except Exception:
            return JsonResponse({'status': 500,
                                'message': 'Unexpected error occurred \
                                while updating emoji, Please contact us!!!'},
                            status=500)


class GenericObjectDeleteView(DeleteView):
    """
    View class for deleting a generic object based on the URL parameters.
    """
    def get_object(self, queryset=None):
        """
        Retrieve the object to be deleted based on the URL parameters.

        Returns:
            Model: The object to be deleted.
        """
        try:
            # Get the model class based on the URL parameter
            model_name = self.kwargs['model']
            model = apps.get_model(app_label='group_chat',
                                   model_name=model_name)

            # Get the object to be deleted
            obj_pk = self.kwargs['pk']
            obj = get_object_or_404(model, pk=obj_pk)

            return obj
        except (LookupError, ValueError, KeyError):
            return JsonResponse(
                {'status': 'error',
                 'message': f'Error retrieving object'})

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests to delete an object.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: JSON response indicating the status of the operation.
        """
        try:
            # Get the object to be deleted
            obj = self.get_object()
            model_name = obj.__class__.__name__

            # Delete the object
            obj.delete()
            # Override the delete method to return a JSON response
            return JsonResponse({'status': 'success',
                                 'message': f'{model_name[:-6]} deleted'})
        except Exception:
            return JsonResponse({'status': 500,
                                 'message': 'Unexpected error occurred while deleting object,\
                                 Please contact us!!!'},
                                status=500)

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the template.

        Returns:
            dict: A dictionary containing context data.
        """
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model']
        return context


class SavePostView(View):
    """
    View class for saving a post for a user.
    """
    def post(self, request, post_id):
        """
        Handle POST requests to save a post for the user.

        Args:
            request (HttpRequest): The HTTP request object.
            post_id (int): The ID of the post to be saved.

        Returns:
            JsonResponse: JSON response indicating the status of the operation.
        """
        try:
            if not request.is_ajax():
                raise PermissionDenied
            # Retrieve the post using its ID
            post = get_object_or_404(PostsModel, id=post_id)

            # Check if the post is already saved by the user
            if SavedPost.objects.filter(user=request.user, post=post).exists():
                return JsonResponse({'status': 'Error',
                                     'message': 'Post already saved'})

            # Save the post for the user
            saved_post = SavedPost(user=request.user, post=post)
            saved_post.save()

            return JsonResponse({'status': 'Success',
                                 'message': 'Post saved'}, status=200)
        except PermissionDenied:
            return render(request, '403.html')
        except PostsModel.DoesNotExist:
            # Handle the case where the specified post does not exist
            return JsonResponse({'status': 'Error',
                                 'message': 'Post does not exist'}, status=404)
        except PermissionDenied:
            return render(request, '403.html')
        except Exception:
            return JsonResponse({'status': 500,
                                 'message': 'Unexpected error occurred while saving post,\
                                 Please contact us!!!'},
                                status=500)
