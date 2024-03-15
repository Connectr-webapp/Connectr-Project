// Theses variables/functions are in another js folder and are global the line below is to let jshint know
/* global EmojiPicker, ajaxRequest, displayMessage,deleteObject, summernoteEnhancerEditPost, summernoteEnhancerPosts, startWebSocket */
// Variables
//url for adding or removing emojis
let emojiUrl = null;
// emoji picker class object
let emojiPicker = new EmojiPicker();
// boolean to check if user scrolled to top
let scrolledToTop = false;
// large screen size breakpoint
const LG_BRAKE_POINT = 1300.98;
let prevPageNum = null;
let lastPageNum = null;
let paginatedPostsUrl = null;


///////////////// event listeners ////////////////////////////


//event listener for the comments links on each post
$('main').on('click', '.comments-link', function(event) {
    event.preventDefault();
    let url = $(this).attr('href');  // Use $(this) to access the clicked element
    ajaxRequest(url, 'GET', '#post-comments', null, function(response){
        $('#post-comments').html(response);
    });

    if(window.innerWidth < LG_BRAKE_POINT){
        $('#channel-posts').removeClass('d-flex');
    }
    $('#post-comments').addClass('d-flex');
});

// button for hiding the comments list
$('main').on('click', '.comments-close-btn', function() {
    if(window.innerWidth < LG_BRAKE_POINT){
        $('#channel-posts').addClass('d-flex');
    }
    $('#post-comments').removeClass('d-flex');
    $('#post-comments').html('');
});

// Click event for the x button to close posts 
$('main').on('click', '.posts-close-btn', function() {
    $('#channel-posts').removeClass('d-flex');
    $('#channel-links-container').removeClass('d-none');
    $('#nav-bar').removeClass('d-none');
    $('header').removeClass('d-none');
});

// event listener for the add user button to 
// shows when user is not a channel member
$('main').on('submit', '#add-user-form', function(event) {
    event.preventDefault();
    let url = $(this).attr('action');
    // send post request to add user
    ajaxRequest(url, 'POST', '#channel-posts', null, function(response){
        $('#overlay').addClass('d-none');
        displayMessage(response, '#channel-posts');
    });
});

// event listener for the delete button on post and comments
$(document).on('click', '.delete-btn', function() {
    // Get the URL of the image
    let deleteUrl = $(this).data('delete-url');
    // get card to be deleted
    let cardBeingDeleted = $(this).closest('.card');
    deleteObject(deleteUrl, cardBeingDeleted, 'post', '#channel-posts');

    if($(cardBeingDeleted)[0].className.includes('post')){
        $('.comments-close-btn').click();
    }
});

// Attach a click event handler to the 'main' element, specifically for elements with the class 'save-post-btn'
$('main').on('click', '.save-post-btn', function(event) {
    // Prevent the default behavior of the click event (e.g., preventing form submission)
    event.preventDefault();

    // Get the URL for saving the post from the 'data-save-post-url' attribute of the clicked element
    let savePostUrl = $(this).data('save-post-url');

    // Make an AJAX request to save the post
    ajaxRequest(savePostUrl, 'POST', '#channel-posts');
});

// listener for edit button on posts and comments dropdown menu
$('main').on('click', '.edit-btn', function(event) {
    // cancel any other post that is in edit mode
    if($('.cancel-edit').length > 0){
        $('.cancel-edit').click();
    }else if($('.edit-post').length > 0 ){
        $('.card.edit-post').removeClass('edit-post');
    }
    // Find the closest ancestor with the class 'card'
    var card = $(this).closest('.card');
    let carbody = card.find('.card-body').html();
    let cardText = card.find('.card-text').html();
    let cardImages = card.find('.post-images').html();
    card.addClass('edit-post');
    let postId = card.data("post-id");
    let editPostUrl = card.data('post-url');
    card.find('.card-body').html('');
    // Append the HTML structure to the body
    editPostUrl += postId + '/';
    summernoteEnhancerEditPost.init('.edit-post .card-body', editPostUrl);

    summernoteEnhancerEditPost.addToSummernoteeditorField(cardText);

    $('.edit-post .summernote-btn-bottom .cancel-submit').prepend('<button class="cancel-edit">Cancel</button>');
    
    $('main').on('click', '.cancel-edit', function(event) {
        event.preventDefault();
        $('.edit-post .card-body').html(carbody);
        $('.card.edit-post').removeClass('edit-post');
    });

    if(cardImages){
        $(cardImages).each(function () {
            let src = $(this).attr('src');
            if(src != undefined){
                summernoteEnhancerEditPost.addimageToSummernote(src);
            }
        }); 
    }
});

////////////////////////// functions for posts ///////////////////////////////////

$('main').on('click', '.load-new-posts', function(){
    let newPostsUrl = paginatedPostsUrl.replace(/0(?!.*0)/, lastPageNum);
    $(this).addClass('d-none');
    ajaxRequest(newPostsUrl, 'GET', '#channel-posts', null, function(response){
        // Update the div with the returned template
        $('#posts-list').html(response);
        autoScroll(true);
    });
});

/**
 * Load older posts when scrolling to the top of the page.
 * This function is triggered by a scroll event.
 */
function loadOldPosts(){
    paginatedPostsUrl = $('#posts-list').data('posts-url');
    let $scrollElement = $(this);

    // Attach scroll event to load older posts when scrolling to the top
    if ($scrollElement.scrollTop() === 0 && !scrolledToTop && prevPageNum != "") {
        scrolledToTop = true;
        let olderPostsUrl = paginatedPostsUrl.replace(/0(?!.*0)/, prevPageNum);
        ajaxRequest(olderPostsUrl, 'GET', '#channel-posts', null, function(response){
            // Update the div with the returned template
            $('#posts-list').prepend(response);
            autoScroll();
        });
    }else if($scrollElement.scrollTop() > $scrollElement[0].scrollHeight - $scrollElement.innerHeight()-2 && lastPageNum != ""){
        let loadPostsBtn = $('.load-new-posts');
        loadPostsBtn.removeClass('d-none');
    }
}


/**
 * Auto-scroll function for handling automatic scrolling in a chat application.
 *
 * @param {boolean} bottomBool - A boolean indicating whether to scroll to the bottom (true) or to a specific post index (false).
 */
function autoScroll(bottomBool, id) {
    //get the post count
    let postCount = $('#channel-posts .scrollable-div .card').length;

    let container = $('#channel-posts .scrollable-div');

    //get the index of the last post before the older posts being appended
    let postAtIndex = $('#channel-posts .scrollable-div .card').eq(9); 
    // scroll to post at index above if there are more 10 else scroll to bottom
    if(postCount >= 20 && !bottomBool){
        // Scroll to the 10th post
        $('#channel-posts .scrollable-div').animate({ scrollTop: postAtIndex.offset().top }, 'fast');
    }else if (id){
        // scroll to the saved post
        let targetPost = $(`#channel-posts .scrollable-div .card[data-post-id="${id}"]`);

        let offsetRelativeToContainer = targetPost.offset().top - container.offset().top;
        container.animate({ scrollTop: offsetRelativeToContainer  }, 'fast');
        // Set multiple CSS properties for the targetPost element
        targetPost.css({
            'border': '2px solid green', 
        });

        $('#channel-posts .scrollable-div').animate({ scrollTop: targetPost.offset().top }, 'fast');

    }else  {
        $('#channel-posts .scrollable-div').animate({ scrollTop: $('.scrollable-div')[1].scrollHeight }, 'fast');
    }
    scrolledToTop = false;
}

//  function gets called when user changes group
function changeGroup(){
    if ($('.card').length < 10 && prevPageNum != "") {
        let olderPostsUrl = $('#posts-list').data('posts-url').replace(/0(?!.*0)/, prevPageNum);
        ajaxRequest(olderPostsUrl, 'GET', '#channel-posts', null, function(response){
            $('#posts-list').prepend(response);
            autoScroll();
        });
    }
    // Scroll to the bottom of the posts list
    scrollTo();
    $('#posts-list').scroll(loadOldPosts);
    let summernoteUrl = $('#posts-list').data('summernote-url');
    // Initialize summernote enhancer class
    summernoteEnhancerPosts.init('#channel-posts', summernoteUrl);
     // Get the channel id using a Django template literal for use in the JS file and for the websocket
    let channel_id = $('#posts-list').data('channel-id'); 
    
    // Start the WebSocket for channel posts
    startWebSocket('channel_posts', channel_id);
}

///////////////// Emoji functionality //////////////////////
// event listener for the emoji button on posts and comments
$('main').on('click', '.card-emoji-btn', function(event) {
    event.preventDefault();
    emojiUrl = $(this).data('emoji-url');
    emojiPicker.addListener(event, emojiPickerCallback);
    emojiPicker.$panel.show();
});

// event listener for emojis that are added to posts or comments
$('main').on({
    click: function(event) {
        event.preventDefault();
        const emojiCode = $(this).data('emoji-code');
        const url = $(this).data('emoji-url');
        const self = this;
        let data = {
            emoji_colon_name: emojiCode,
        };
         // Send a post request to Django with the emoji information
    ajaxRequest(url, 'POST', 'main', data, function(response){
        updateEmoji(emojiCode, null, self, response, url);
    });
    },
    mouseenter: function() {
        if(window.innerWidth > LG_BRAKE_POINT){
            $(this).css('cursor', 'pointer');
            $(this).siblings('.emoji-user-count-modal').removeClass('d-none');
        }
        
    },
    mouseleave: function() {
        if(window.innerWidth > LG_BRAKE_POINT){
            $(this).css('cursor', 'pointer');
            $(this).siblings('.emoji-user-count-modal').addClass('d-none');
        }
    }
}, '.added-emoji-btn');

/**
 * Callback function triggered when a user clicks an emoji in the emoji picker.
 *
 * This function sends a post request to the Django server with the selected emoji's
 * information.
 *
 * @param {Object} emoji - The emoji object representing the clicked emoji.
 */
function emojiPickerCallback(emoji) {
    // Extract the emoji's colon name
    let emojiColonName = emoji.alt;

    let data = {
        emoji_colon_name: emojiColonName,
    };
    // Send a post request to Django with the emoji information
    ajaxRequest(emojiUrl, 'POST', 'main', data, function(response){
        updateEmoji(emojiColonName, emoji, null, response, emojiUrl);
    });
}

/**
 * Update Emoji function for handling the response and updating the emoji UI.
 *
 * @param {string} emojiColonName - The colon-style name of the emoji (e.g., ':smile:').
 * @param {string} emojiImg - The HTML representation of the emoji image.
 * @param {HTMLElement} clickedBtn - The button element that was clicked to trigger the update.
 * @param {object} response - The response object containing the status of the update.
 * @param {string} url - The URL associated with the emoji update.
 */
function updateEmoji(emojiColonName, emojiImg, clickedBtn, response, url) {
    let id = url.match(/\d+/g);
    let spanElement;
    let emojiUlClass = `.emoji-list${id}`;
    const emojiClass = emojiColonName.slice(1,-1);
    if(clickedBtn){
        spanElement = $(clickedBtn).find('span');
    }
    let currentNumber = null;
    // Handle success
    switch (response.status) {
        case "added":
            let em = $(emojiImg).prop('outerHTML');

            let newLi = $(`
                <li class="list-inline-item mr-2">
                    <button class="added-emoji-btn btn ${emojiClass}" data-emoji-url="${url}" 
                            data-target="#emojiModal${id}" 
                            data-emoji-code="${emojiColonName}">
                            ${em}
                        <span></span>
                    </button>
                    <!-- Small Box Modal -->
                    <div class="emoji-user-count-modal d-none" id="emojiModal${id}">
                        <div class="modal-dialog modal-sm">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="emojiModalLabel">${em}</h5>
                                </div>
                                <div class="modal-body">
                                    <p>You reacted with ${emojiColonName}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </li>
            `);
            $(emojiUlClass).append(newLi);
            break;
        case "decremented":
            currentNumber = parseInt(spanElement.html(), 10);

            if (!isNaN(currentNumber)) {
                // Check if currentNumber is a valid number

                // Subtract 1 from the current number
                let newNumber = currentNumber - 1;
                if (newNumber > 1) {
                    // Update the HTML content of the span element with the new number
                    spanElement.html(newNumber);
                } else {
                    spanElement.html('');

                }
            }
            break;
        case "incremented":

            currentNumber = parseInt(spanElement.html(), 10);
            if (!isNaN(currentNumber)) {
                // add 1 to the current number
                let newNumber = currentNumber + 1;
                // Update the HTML content of the span element with the new number
                spanElement.html(newNumber);
            } else {
                spanElement.html(2);
            }

            break;
        case "removed":
                $(emojiUlClass).find(`.${emojiClass}`).parent().remove();
    }
}