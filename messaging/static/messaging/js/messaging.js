let msgToBeDel = null;
let deleteUrl = null;
let deleteModelBody = null;
const emojiPicker = new EmojiPicker();
let messageTags = null;
let emojiUrl = null;



// ////////////////////////////// inbox functionality ////////////////////////////

$('#messages-list-container').on('click', '.close-messages-btn', function(){
    $('.inbox-container').removeClass('d-none');
    $('#messages-list-container').addClass('d-none');
    $('#messages-list-container').removeClass('d-flex');
    $('#nav-bar').removeClass('d-none');
    $('header').removeClass('d-none');
});

$('.inbox-container').on('click', '.message-link', function(e){
    e.preventDefault();
    let url = $(this).closest('.message-link').data('message-list-url');
    $('.message-link').removeClass('active');
    $(this).addClass('active');
    ajaxRequest(url, 'GET', '#messages-list-container', null, function(response){
        $('#messages-list-container').html(response);
        //autoScroll()
        if(window.innerWidth < 991.98){
            $('.inbox-container').addClass('d-none');
            $('#messages-list-container').removeClass('d-none');
            $('#messages-list-container').addClass('d-flex');
            $('#nav-bar').addClass('d-none');
            $('header').addClass('d-none');
        }
    });
});

$('.inbox-container').on('click', '.delete-conversation', function(e){
    const url = $(this).data('url');
    let users_name = $(this).closest("li").find("h3").text();
    const convId = $(this).data('conv-id');
    let header = `<h3>Are you sure you want to delete your conversation with ${users_name}</h3>`;
    let body = `
        <form>
            <div class="input-group text-center d-flex justify-content-between">
                <button type="button" class="btn btn-oval btn-info" 
                data-dismiss="modal" aria-label="Close">No</button>

                <button id="delete-conversation-btn" 
                class="btn btn-oval btn-info" data-dismiss="modal" 
                type="button" data-url="${url}"
                data-conv-id="${convId}">Yes</button>
            </div>
        </form>`;
    showModal(header, body);
});


$('body').on('click', '#delete-conversation-btn', function(e){
    const url = $(this).data('url');
    const convId = $(this).data('conv-id');
    ajaxRequest(url, 'DELETE', '.messaging', null);
    $(`.msg${convId}`).remove();
    $('#messages-list-container').empty();
});


// event listener for the delete button on post and comments
$('#messages-list-container').on('click', '.message-delete-btn', function() {
    let deleteUrl = $(this).data('delete-url');
    let msgToBeDel = $(this).closest('.message');
    deleteObject(deleteUrl, msgToBeDel, 'message', '.messaging');
});


// listener for edit button on posts and comments dropdown menu
$('main').on('click', '.edit-btn', function(event) {
    // cancel any other post that is in edit mode
    let cancelBtnTxt;
    if($('.cancel-edit').length > 0){
        $('.cancel-edit').click();
    }else if($('.edit-post').length > 0 ){
        $('.edit-post').removeClass('edit-post');
    }
    // Find the closest ancestor with the class 'card'
    var card = $(this).closest('.message');
    let cardText = card.find('.message-text').html();
    let cardImages = card.find('.post-images').html();
    card.addClass('edit-post');
    
    let editPostUrl = $('#message-list').data('edit-url');
    let msgId = card.data('msg-id');
    editPostUrl = editPostUrl.replace(/0(?!.*0)/, msgId);

    card.find('.message-text').html('');
    card.find('.post-images').html('');
    // Append the HTML structure to the body
    
    summernoteEnhancerEditPost.init('.edit-post .message-text', editPostUrl);
    summernoteEnhancerEditPost.addToSummernoteeditorField(cardText);
    if(window.innerWidth > 991.98){
        cancelBtnTxt = 'Cancel'
    }else{
        cancelBtnTxt = 'X'
    }

    $('.edit-post .summernote-btn-bottom .cancel-submit').prepend(`<button class="cancel-edit">${cancelBtnTxt}</button>`);
    
    $('main').on('click', '.cancel-edit', function(event) {
        event.preventDefault();
        $('.edit-post .message-text').html(cardText);
        $('.edit-post .post-images').html(cardImages);
        $('.message').removeClass('edit-post');
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
        const url = $(this).data('emoji-url');
        const emojiCode = $(this).data('emoji-code');
        const self = this;
        let data = {
            emoji_colon_name: emojiCode,
        };
         // Send a post request to Django with the emoji information
    ajaxRequest(url, 'POST', 'main', data, function(response){
        updateEmoji(emojiCode, null, self, response, emojiUrl);
    });
    },
    mouseenter: function() {
        if(window.innerWidth > 991.98){
            $(this).css('cursor', 'pointer');
            $(this).siblings('.emoji-user-count-modal').removeClass('d-none');
        }
        
    },
    mouseleave: function() {
        if(window.innerWidth > 991.98){
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


$('body').on('input', ".panel-search-form input", function(e){
    e.preventDefault();
    if($(this).val() == '@'){
        autoComplete(".panel-search-form", messageTags, function(tag){
            let targetDiv = $(`[data-userId="${tag.id}"]`);
            targetDiv.click();
        });
    }
});

