"""
Views for handling user profile.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError, OperationalError
from group_chat.models import SavedPost, PostsModel
from .models import UserProfile
from .forms import ProfileImageForm, EditProfileForm, StatusForm
from .forms import ContactForm


# pylint: disable=no-member
@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    """
    View for displaying and updating user profiles.
    """
    template_name = 'user_profile/user_profile.html'

    def get(self, request, status=None):
        """
        Handle GET requests to display the user profile.

        Returns:
            HttpResponse: The rendered user profile page.
        """
        try:
            user_profile = get_object_or_404(UserProfile, user=request.user)
            saved_posts = SavedPost.objects.filter(user=request.user)
            posts = [saved_post.post for saved_post in saved_posts]

            edit_profile_form = EditProfileForm(instance=user_profile)
            profile_image_form = ProfileImageForm(instance=user_profile)
            status_form = StatusForm(instance=user_profile)
            context = {
                'user_profile': user_profile,
                'Edit_profile_form': edit_profile_form,
                'profile_image_form': profile_image_form,
                'status_form': status_form,
                'posts': posts,
            }

            if status:
                context['status'] = status
            return render(request, self.template_name, context)
        except UserProfile.DoesNotExist:
            return redirect('404.html', status=404)
        except Exception:
            return redirect('contact',
                            'There has been an unexpexted error\
                            , contact us or create a new profile')

    def post(self, request):
        """
        Handle POST requests to update the user profile.

        Returns:
            HttpResponse: The rendered user profile page or a redirect.
        """
        try:
            edit_profile_form = EditProfileForm(
                request.POST,
                instance=request.user.userprofile
            )

            if edit_profile_form.is_valid():
                edit_profile_form.save()

                return redirect('user_profile', status='success')

            return redirect('user_profile', status='error')
        except Exception:
            return redirect('contact',
                            'There has been an Unexpected error \
                            updating your profile! Please Contact Us!!!')


@method_decorator(login_required, name='dispatch')
class ViewUserProfile(View):
    """
    View for displaying and updating user profiles.
    """
    template_name = 'user_profile/view-user-profile.html'

    def get(self, request, user_id):
        """
        Handle GET requests to display the user profile.

        Returns:
            HttpResponse: The rendered user profile page.
        """
        try:
            # Ensure the request is an AJAX request
            if not request.is_ajax():
                raise PermissionDenied
            user_profile = get_object_or_404(UserProfile, id=user_id)

            context = {
                'user_profile': user_profile,
            }
            return render(request, self.template_name, context)

        except PermissionDenied:
            return JsonResponse(
                {'status': 'Error',
                 'message': 'Permission Denied'},
                status=403
            )
        except Exception:
            return JsonResponse(
                {'status': 500,
                 'message': 'Unexpected error retrieving \
                    user profile, Please Contact us!!!'},
                status=500
            )


@require_POST
@login_required
def update_profile_image(request):
    """
    Update the profile picture of the currently logged-in user.

    Returns:
        JsonResponse: A JSON response indicating success or failure.
    """
    try:
        # Ensure the request is an AJAX request
        if not request.is_ajax():
            raise PermissionDenied
        form = ProfileImageForm(request.POST,
                                request.FILES,
                                instance=request.user.userprofile)

        if form.is_valid():
            image = form.save()
            return JsonResponse(
                {'success': 'image',
                 'message': image.profile_picture.url},
                status=200)

        return JsonResponse(
            {'status': 'error',
             'message': f'Error updating profile picture: {form.errors}'},
            status=400)

    except PermissionDenied:
         return JsonResponse(
            {'status': 'error',
                'message': 'Permission denied'},
            status=500)
    except Exception:
        return JsonResponse(
            {'status': 500,
                'message': 'Unexpected Error updating \
                profile picture, Please contact us'},
            status=500)


@require_POST
@login_required
def update_status(request):
    """
    View for updating the user's status.

    Args:
    - request: HTTP request object.

    Returns:
    - JsonResponse: JSON response indicating success or failure.
    """
    try:
        # Ensure the request is an AJAX request
        if not request.is_ajax():
            raise PermissionDenied
        form = StatusForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            status = form.save()
            return JsonResponse(
                {'status': 'success',
                 'message': status.status},
                status=200)
        return JsonResponse(
            {'status': 'error',
             'message': f'Error updating status: {form.errors}'},
            status=400)
    except PermissionDenied:
        return render(request, '403.html')
    except Exception:
        return JsonResponse({'status': 500,
                             'message': 'Unexpected error updating\
                             status, Please contact us!!!'},
                            status=500)


@require_POST
@login_required
def remove_saved_post(request, post_id):
    """
    Remove a saved post for the currently logged-in user.

    Args:
        post_id (int): The ID of the post to be removed from saved posts.

    Returns:
        JsonResponse: A JSON response indicating success or failure.
    """
    try:
        # Ensure the request is an AJAX request
        if not request.is_ajax():
            raise PermissionDenied
        # Retrieve the post instance
        post = get_object_or_404(PostsModel, id=post_id)

        # Check if the post is saved by the user
        saved_posts = SavedPost.objects.filter(user=request.user,
                                               post=post)

        if saved_posts.exists():
            # If the post is saved, remove it
            saved_posts.delete()
            return JsonResponse({'status': 'Success',
                                 'message': 'Post removed'},
                                status=200)

        # If the post is not saved, return an error
        return JsonResponse({'status': 'Error',
                             'message': 'Saved Post not found'},
                            status=400)
    except PermissionDenied:
        return render(request, '403.html')
    except PostsModel.DoesNotExist:
        return JsonResponse({'status': 'Error',
                             'message': 'Post not found'},
                            status=404)
    except Exception:
        # Return an error for non-POST requests
        return JsonResponse({'status': 500,
                             'message': 'Unexpected erro removing\
                             saved post, Please contact us'},
                            status=500)


def get_all_users_profiles(request):
    """
    view for retrieving all users profiles and creating a list
    of username, id and profile_picture url for search bar in
    the header section of site
    """
    try:
        # Ensure the request is an AJAX request
        if not request.is_ajax():
            raise PermissionDenied
        user_profiles = UserProfile.objects.all().values('username',
                                                         'id',
                                                         'profile_picture')
        return JsonResponse(list(user_profiles), safe=False)
    except PermissionDenied:
        return render(request, '403.html')
    except (DatabaseError, OperationalError):
        return JsonResponse({'status': 'Error',
                             'message': 'Database error'},
                            status=500)
    except Exception:
        return JsonResponse({'status': 500,
                             'message': 'Unexpected error retrieving\
                             user profiles, Please contact us!!!'},
                            status=500)


@require_POST
@login_required
def delete_user_account(request):
    """
    Deletes the user account of the authenticated user.

    Parameters:
    - request: The HTTP request object.

    Returns:
    A JSON response indicating the status of the operation.
    """
    try:
        # Ensure the request is an AJAX request
        if not request.is_ajax():
            raise PermissionDenied

        # Retrieve the authenticated user
        user = get_object_or_404(get_user_model(),
                                 id=request.user.id)

        # Delete the user account
        user.delete()

        return JsonResponse({'status': 'Success',
                             'message': 'Account Deleted'},
                            status=200)
    except get_user_model().DoesNotExist:
        return JsonResponse(
            {'status': 'Error',
             'message': 'User not found'},
            status=404)
    except PermissionDenied:
        return render(request, '403.html')
    except Exception:
        # Handle exceptions and return an appropriate error response
        return JsonResponse({'status': 500,
                             'message': 'Error: deleting your account, please contact us!!!'},
                            status=500)


def contact_view(request, error=None):
    """
    View for handling contact form submissions.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered contact form page.
    """
    try:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                sender = form.cleaned_data['email']
                recipients = [settings.DEFAULT_FROM_EMAIL]
                send_mail(subject, message, sender, recipients)

                return redirect('contact', 'Success')
            return redirect('contact', form.errors)
        else:
            form = ContactForm()

            # Assign an empty dictionary to 'message' to
            # avoid KeyError in the next request

            context = {'form': form}
            if error == 'Success':
                context['success'] = 'Your message has been sent \
                    we will contact you in the next 24hr'
            elif error:
                context['message'] = error
            return render(request, 'user_profile/contact.html', context)

    except Exception:
        return render(request, '500.html', status=500)
