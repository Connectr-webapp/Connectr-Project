// Theses variables/functions are in another js folder and are global the line below is to let jshint know
/* global EmojiPicker, ajaxRequest, autoScroll */
/**
 * Toggle the visibility of the messages list when the button is clicked.
 * 
 * This function handles the click event on elements with the class 'toggleLinksButton'.
 * It toggles the visibility of the target element specified by the 'data-target' attribute
 * and rotates the icon inside the clicked button.
 */
$('.toggleLinksButton').click(function() {
    var target = $(this).data('target');
    $(target).toggleClass('d-none');
    $(this).find('i').toggleClass('fa-rotate-90');
});

/**
 * 
 * This function handles the click event on channel links 
 * It prevents the default behavior of the link, updates the active channel, and performs an AJAX request
 * to load the channel posts.
 */
$('main').on('click', '.channel-link', function(event) {
    event.preventDefault();

    $('.channel-link').removeClass('active');

    $(this).find('.unread-indicator').remove();
    $(this).addClass('active');
    let url = event.currentTarget.href;
    ajaxRequest(url, 'Get', '#channel-posts', null, function(response){
        $('#channel-posts').html(response);
        autoScroll();
    });

    if(window.innerWidth < 991.98){
        $('#channel-posts').addClass('d-flex');
        $('#channel-links-container').addClass('d-none');
        $('#nav-bar').addClass('d-none');
        $('header').addClass('d-none');
    }else{
        $('#channel-posts').addClass('d-flex');
        $('#post-comments').removeClass('d-flex');
    }
   
});