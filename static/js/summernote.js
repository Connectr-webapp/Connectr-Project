// Theses variables/functions are in another js folder and are global the line below is to let jshint know
/* global EmojiPicker, displayMessage, ajaxRequest, autoComplete */

/**
 * SummernoteEnhancer class for enhancing the functionality of Summernote editors in a web application.
 * This class provides methods to initialize, display, and handle events related to Summernote editors.
 *
 * Properties:
 * - sharedChannelUsers: Array containing shared channel user information.
 * - emojiImgs: Null or emoji images.
 * - imgUrl: Null or image URL.
 *
 * Methods:
 * - constructor(): Initializes class properties.
 * - init(divToLoadIn, djangoUrl, csrf_token): Initializes SummernoteEnhancer with the specified parameters.
 * - tagUser(): Tags a user in the Summernote editor.
 * - submitForm(djangoUrl): Submits the form data to Django.
 * - addToSummernoteeditorField(content): Adds content to the Summernote editor.
 * - addimageToSummernote(src): Adds an image to the Summernote editor.
 * - resizeEditor(): Adjusts the height of the editor.
 * - uploadImage(file, editor, welEditable): Uploads an image using AJAX.
 * - createForm(csrf_token): Creates the structure of the Summernote editor form.
 *
 * Instances:
 * - summernoteEnhancerPosts: Instance for handling Summernote editors in posts.
 * - summernoteEnhancerComments: Instance for handling Summernote editors in comments.
 * - summernoteEnhancerEditPost: Instance for handling Summernote editors in editing posts.
 */
class SummernoteEnhancer {
  static emojiImgs = null;
  static imgUrl = null;

  constructor() {
    this.divToLoadIn = null;
    this.$sn = null;  // Initialize as null
    this.snSubmitForm = null;
    this.djangoUrl = null;
    this.snForm = null;
    this.divsection = null;
    this.$storeText = null;
    this.uploadImageUrls = [];
    this.parentDiv = '';
    this.emojiPicker = null;
    this.atRemoved = null;
  }

  /**
   * Initializes SummernoteEnhancer with the specified parameters.
   *
   * @param {string} divToLoadIn - The ID or class of the container where Summernote editor is loaded.
   * @param {string} djangoUrl - The Django URL for handling form submission.
   * @param {string} csrf_token - The CSRF token for form submission.
   */
  init(divToLoadIn, djangoUrl) {
    let self = this;
    this.divToLoadIn = divToLoadIn;
    this.djangoUrl = djangoUrl;
    this.emojiPicker = new EmojiPicker();


    this.createForm();

    this.$sn = $(`${this.divToLoadIn} textarea`);  

    this.$sn.summernote({
      toolbar: [
          ['style', ['bold', 'italic', 'strikethrough', 'underline']],
          ['para', ['ul', 'ol', 'paragraph']],
          ['insert', ['link', 'picture']],
          ['misc', ['codeview', 'undo', 'redo']],
      ],
      width: '100%',
      attachment_require_authentication: true,
      placeholder: 'Type @ for users # for channels',
      focus: true,
      callbacks: {
          onInit: function () {
              // Attach an input event handler to the Summernote editor
              self.$sn.next().find('.note-editable').on('input', function (e) {
                  let $snText = $('<p>').html(self.$sn.summernote('code')).text();
                  if (($snText.slice(-1) === '@' || $snText.slice(-1) === '#')&& ($snText.slice(-2, -1) === ' ' || $snText.slice(-2, -1) === ';' || $snText.slice(-2, -1) === '')){
                      self.tagUser($snText.slice(-1));
                  }else{
                    self.atRemoved = self.$sn.summernote('code');
                  }
                  

                  if(e.target.lastChild){
                    self.parentDiv = $(e.target.lastChild.classList);              
                  }
              }); 
          },
          // image upload callback 
          onImageUpload: function(files) {
            self.uploadImage(files[0],self.$sn);
          }
        },  
    });

    $('.note-editable').attr('aria-label', 'editor input');
    // summernote submit button
    this.snSubmitForm = $(`${this.divToLoadIn} .sn-submit-btn`);
    // summernote form 
    this.snForm = $(`${this.divToLoadIn} .sn-form`);
    // submit btn listener
    this.snSubmitForm.click((event) => {
      event.preventDefault();
      // Check if the content is empty or meets your criteria
      let $summernoteContent = self.$sn.summernote('code');
      let tempDiv = $('<div>');
      tempDiv.html($summernoteContent);
      
      tempDiv.find('img').each(function() {

        let altText = $(this).attr('alt');

        if (!altText.endsWith(":")) {
            altText = ":" + altText + ":";
            $(this).replaceWith(altText);
        }else{
          $(this).replaceWith($(this).attr('alt'));
        }
      });
      self.$sn.summernote('code', tempDiv.html());
    
      let plainText = tempDiv.text().trim();
      if (!plainText) {
        displayMessage({'status': 'summernote-error'});
      }else{
        this.submitForm(self.djangoUrl);
      }
  });

    this.divsection = $(this.divToLoadIn);

    //@ symbol event listener
    $(`${this.divToLoadIn} .at-symbol`).click(() => {
      let atSymbol = document.createTextNode(`@`);
      this.$sn.summernote(`editor.insertNode`, atSymbol);
      this.tagUser('@');      
    });

    $(`${this.divToLoadIn} .add-image`).click(() => {
      $(`${this.divToLoadIn} .note-insert button`)[1].click();
    });

    $(`${this.divToLoadIn} .note-resizebar`).on('mousedown',() => {
      this.resizeEditor();
    });

    $(`${this.divToLoadIn} .note-toolbar button`).on('click',(e) => {
      e.preventDefault();
      $(e.currentTarget).addClass('btn-info');
    });

    $(`${this.divToLoadIn} .note-toolbar .note-misc button:first`).off().addClass('codeview');

    $(`${this.divToLoadIn} .codeview`).on('click', function(e) {
      e.preventDefault();
      $(this).toggleClass('button-color');

      let txt = self.$sn.summernote('code');
      let txtContent = $(txt).text();
      let pElement = null;
      if(self.parentDiv[0] === 'codeview-div'){
        pElement = $(`<p class="p-1"></p>`)[0];
        self.$sn.summernote('editor.insertNode', pElement);
        self.parentDiv = '';
      }else{
        if(txtContent.length === 0){
          pElement = $(`<p class="codeview-div p-2">${txtContent}</p>`)[0];
          self.$sn.summernote(`code`, pElement );
        }else{
          pElement = $(`<p class="codeview-div p-2"></p>`)[0];
          self.$sn.summernote(`editor.insertNode`, pElement );
        }
      }
      self.$sn.summernote(`focus`);
  });

    //overlay event listener to close modals
    $(`.hide-modal`).click(() => {
      $(`${this.divToLoadIn} .tag-name-modal`).hide();
      $(`.hide-modal`).hide();
    });


    // Add this code to bind the click event of existing button
    $(`${this.divToLoadIn} .emoji-popup-btn`).on('click', function (event) {      
      $(`.hide-modal`).show();
        self.emojiPicker.addListener(event, function(emoji){
        self.$sn.summernote('editor.insertNode', emoji);
        $(`.hide-modal`).hide();
      });
      self.emojiPicker.$panel.show();
    });

    $(document).on('click', '.delete-img-icon', function() {
      // Get the URL of the image
      let url = $(this).parent().find('img').attr('src');
 
      // Iterate over each element in the array
      self.uploadImageUrls.forEach(function(uploadedImg, index) {
         if (uploadedImg === url) {
             // Remove the element at the corresponding index
             self.uploadImageUrls.splice(index, 1);
         }
      });
        // Remove the parent element
      $(this).parent().remove();
    });
  
  }

  /**
   * Tags a user in the Summernote editor.
   */
  tagUser(symbol) {
    let self = this;
      if(symbol === '@'){
        let profileTags = [];
        let userProfileUrl = $('body').data('user-profiles');
  
        ajaxRequest(userProfileUrl, 'GET', 'body', null, function(response){
          response.forEach(function(profile) {
            profileTags.push({label: profile.username, id: profile.id, profile_img: profile.profile_picture});
          });
          autoComplete(self.$sn.closest('form'), profileTags, true, function(tag){
            let profileUrl = $('body').data('view-profile-url').replace('0', tag.id);
  
            const tagLink = $('<a>', {
              'data-profile-url': profileUrl,
              text: '@' + tag.label,
              class: 'profile-pic tag-user-link',
              href: '#'
          });
  
          self.$sn.summernote(`code`, '');
  
          $(self.atRemoved).each(function(){
            self.$sn.summernote(`editor.insertNode`, this);
          });
            
          self.$sn.summernote(`editor.insertNode`, tagLink[0]);
        });
      });

      }else if (symbol === '#'){
        let channelTags = [];
        let allChannelsUrl = $('body').data('all-channels');

  
        ajaxRequest(allChannelsUrl, 'GET', 'body', null, function(response){
          response.forEach(function(channel) {
            channelTags.push({label: channel.name, name: channel.name, id: channel.id, url: channel.url });
          });
          autoComplete(self.$sn.closest('form'), channelTags, false, function(tag){
  
            const tagLink = $('<a>', {
              text: '#' + tag.label,
              href: tag.url,
              class: 'tag-user-link'
            });
    
            self.$sn.summernote(`code`, '');
    
            $(self.atRemoved).each(function(){
              self.$sn.summernote(`editor.insertNode`, this);
            });
              
            self.$sn.summernote(`editor.insertNode`, tagLink[0]);
        });
      });
     }
  }

  /**
   * Submits the form data to Django.
   *
   * @param {string} djangoUrl - The Django URL for handling form submission.
   */
  submitForm(djangoUrl){
    const self = this;
    // Serialize the form data
    let formData = this.snForm.serialize();
    if(self.uploadImageUrls.length > 0 ){ // Loop through each URL in uploadImageUrls
      $.each(self.uploadImageUrls, function(index, url) {
          // Check if the URL is not already present in the form data
          if (formData.indexOf(encodeURIComponent(url)) === -1) {
              // Append the URL to the form data
              formData += `&urls[]=${encodeURIComponent(url)}`;
          }
      });
    }

    ajaxRequest(djangoUrl, 'POST', 'body', formData, function(response){
      self.$sn.summernote('code', "");
      $(`${self.divToLoadIn} div.note-editing-area .sn-img`).remove();

    });
  
    self.uploadImageUrls = [];

  }

  /**
   * Adds content to the Summernote editor.
   *
   * @param {string} content - The content to be added.
   */
  addToSummernoteeditorField(content){
    this.$sn.summernote('code', content);
  }

  /**
   * Adds an image to the Summernote editor.
   *
   * @param {string} src - The source URL of the image.
   */
  addimageToSummernote(src){
    this.uploadImageUrls.push(src);
    // Append the image and icon to the specified container
    $(`${this.divToLoadIn} div.note-editing-area`).append(`
      <div class="sn-img">
        <i class="fa-solid fa-x position-absolute delete-img-icon"></i>
        <img src="${src}"  alt="Uploaded Image">
      </div>
    `);    
  }

  /**
   * Adjusts the height of the editor.
   */
  resizeEditor() {
      const fullScreen = 400;
      if($('.note-editable').height() < fullScreen-30){
        $('.note-editable').css({height:` ${fullScreen}px`});
      }else {
        $('.note-editable').css({height:` 50px`});
      }
  }

  /**
   * Uploads an image using AJAX.
   *
   * @param {File} file - The image file to be uploaded.
   * @param {object} editor - The Summernote editor object.
   * @param {object} welEditable - The editable element in the editor.
   */
  uploadImage(file, editor, welEditable) {
      // Create a FormData object to send the file to the server
      let uploadUrl = $('body').data('upload-image');
      var formData = new FormData();
      formData.append("file", file);
      let self = this;

      ajaxRequest(uploadUrl, 'POST', 'body', formData, function(response){
        self.addimageToSummernote(response.url);
      });
  }
  /**
   * Creates the structure of the Summernote editor form.
   *
   */
    createForm(){
      let htmlStructure = `
      <!-- Container for summernote editor -->
      <div class="summernote-form mb-2 px-2">
          <!-- Container for usernames list that the user can tag with @ -->
          <div class="tag-name-modal popup">
              <ul class="channel-users d-flex flex-column ml-3 my-3"></ul>
          </div>
  
          <!-- Summernote editor form -->
          <form class="sn-form" method="post">
              
              <textarea class='d-none' name="post"></textarea>
  
              <!-- Buttons at the bottom of summernote editor emoji,@ and arrow for posting -->
              <div class="summernote-btn-bottom">   

                  <div class="mb-2 ml-2">  
                      <button class="mx-1 add-image d-none" type="button" aria-label="add image button">
                          <span class="fa-solid fa-plus fa-xl" style="color: var(--ci-orange);"></span>
                      </button>
                      <button class="mx-1 mt-1 emoji-popup-btn" type="button" aria-label="emoji button">
                          <span class="fa-regular fa-face-smile fa-xl emoji-btn" style="color: var(--ci-orange);"></span>
                      </button>
                      <button class="mx-1 at-symbol" type="button" aria-label="tagging button">
                          <span class="fa-solid fa-at fa-xl" style="color: var(--ci-orange);"></span>
                      </button>
                      
                  </div>
                  <div class="cancel-submit">   
  
                      <button class="post-arrow-btn mx-3 sn-submit-btn" type="submit" aria-label="send message button">
                          <span class="fa-solid fa-play fa-xl" style="color: var(--ci-orange);"></span>
                      </button>
                  </div>
              </div>
          </form>
      </div>
      `;
      let $htmlStructure = $(htmlStructure);
  
    $(this.divToLoadIn).append($htmlStructure);
       if(window.innerWidth < 575.98){ 
        $('.add-image').removeClass("d-none");
       }
    }


}
/**
 * Instance for handling Summernote editors in posts.
 */
const summernoteEnhancerPosts = new SummernoteEnhancer();
/**
 * Instance for handling Summernote editors in comments.
 */
const summernoteEnhancerComments = new SummernoteEnhancer();

/**
 * Instance for handling Summernote editors in editing posts.
 */
const summernoteEnhancerEditPost = new SummernoteEnhancer();


