// Theses variables/functions are in another js folder and are global the line below is to let jshint know
/* global ajaxRequest, displayMessage, showModal, statusModalBody, profileImgModal */

// This function is executed when the DOM is ready
$(document).ready(function () {
    // Event handler for clicking the 'Edit Profile' button
    $('body').on('click', '.edit-profile-btn', function () {
        // Show the update profile container and hide other elements
        $('.update_profile_container').removeClass('d-none');
        $('.profile-container').addClass('d-none');
        $('#nav-bar').addClass('d-none');
        $('header').addClass('d-none');
    });

    // Event handler for clicking the 'Close Edit Profile' button
    $('body').on('click', '.close-edit-profile-btn', function () {
        // Hide the update profile container and show other elements
        $('.update_profile_container').addClass('d-none');
        $('.profile-container').removeClass('d-none');
        $('#nav-bar').removeClass('d-none');
        $('header').removeClass('d-none');
    });

    // Event handler for clicking the 'View Saved Posts' button
    $('body').on('click', '.view-save-posts-btn', function () {
        // Show the saved posts container and hide other elements on small screens
        $('.saved-posts-container').removeClass('d-none');
        if (window.innerWidth < 991.98) {
            $('.profile-container').addClass('d-none');
            $('#nav-bar').addClass('d-none');
            $('header').addClass('d-none');
        }
    });

    // Event handler for clicking the 'Close Saved Posts' button
    $('body').on('click', '.saved-posts-close-btn', function () {
        // Hide the saved posts container and show other elements on small screens
        $('.saved-posts-container').addClass('d-none');
        if (window.innerWidth < 991.98) {
            $('.profile-container').removeClass('d-none');
            $('#nav-bar').removeClass('d-none');
            $('header').removeClass('d-none');
        }
    });

    // Event handler for clicking the 'Remove Post' button within saved posts
    $('.saved-posts-container').on('click', '.remove-post-btn', function (e) {
        e.preventDefault();
        // Get the URL and post element for removal
        let url = $(this).data('url');
        let post = $(this).closest('.card');
        // Perform AJAX request to remove the post
        ajaxRequest(url, 'POST', '.saved-posts-container', null, function (response) {
            displayMessage(response, '.saved-posts-container');
            post.remove();
        });
    });

    // Event handler for changing the profile picture input
    $('body').on('change', '#id_profile_picture', function (event) {
        var selectedFile = event.target.files[0];
        if (selectedFile) {
            // Get a temporary URL for the selected file and update the profile picture preview
            var imageURL = URL.createObjectURL(selectedFile);
            $('.modal-body .profile_pic').attr('src', imageURL);
        }
    });

    // Event handler for submitting the profile update form
    $('body').on('click', '.sub-form', function (event) {
        event.preventDefault();
        // Get the URL and form data for the AJAX request
        let url = $(this).parent().data('url');
        var formData = new FormData($(this).closest('form')[0]);
        // Perform AJAX request for profile update
        ajaxRequest(url, 'POST', '.profile-container', formData, function (response) {
            // Handle the response and display appropriate messages
            if (response.status === 'success') {
                $('.status').html(`Current Status: ${response.message}`);
                displayMessage(response, '.profile-container');
            } else if (response.success === 'image') {
                $('.profile_pic').attr('src', response.message);
                displayMessage({ 'status': 'success', 'message': 'Profile picture updated' }, '.profile-container');
            } else {
                displayMessage(response, '.profile-container');
            }
        });
    });

    // Event handler for clicking the 'Update Status' button
    $('.status-update-btn').on('click', function () {
        // Show a modal for updating the status
        let statusModalHeader = $(`<div class="d-flex flex-dir-row justify-content-end"><h3 class="mx-auto">Update Your Status</h3>
        <button type="button" class="btn btn-oval btn-warning"
        data-dismiss="modal" aria-label="Close">X</button></div>`);

        showModal(statusModalHeader, statusModalBody);
    });

    // Event handler for clicking the 'Update Profile Picture' button
    $('.profile-img-modal').on('click', function () {
        // Show a modal for updating the profile picture
        let imageModalHeader = $(`<div class="d-flex flex-dir-row justify-content-end"><h3 class="mx-auto">Update Profile Picture</h3>
        <button type="button" class="btn btn-oval btn-warning" 
        data-dismiss="modal" aria-label="Close">X</button></div>`);

        showModal(imageModalHeader, profileImgModal);
    });
});
