// Theses variables/functions are in another js folder and are global the line below is to let jshint know
/* global ConfigStorage, Config */

/**
 * EmojiPicker class for handling emoji selection .
 * This class provides methods to initialize, display, and handle events related to the emoji picker.
 *
 * Properties:
 * - emojiSource: The source URL for emoji images.
 * - icons: Object containing emoji icons information.
 * - reverseIcons: Object containing reverse mapping of emoji icons.
 * - $panel: jQuery object representing the emoji panel.
 * - emojiClickedCallback: Callback function to handle the selected emoji.
 *
 * Methods:
 * - addListener(event, emojiClickedCallback): Adds event listeners for emoji selection.
 * - loadEmojis(): Loads emoji data into the class.
 * - setContainerPos(event): Sets the position of the emoji panel based on the event.
 * - updateEmojisList(index): Updates the list of emojis in the panel based on the selected category.
 * - createdEmojiIcon(emoji): Creates HTML for displaying an emoji icon.
 * - colonToUnicode(emoij): Converts colon-based emoji notation to Unicode.
 * - emojiPanel(): Initializes and displays the emoji panel.
 * - destroy(): Destroys the emoji picker, removing its elements from the DOM.
 */
class EmojiPicker {

    static emojiSource = null;

    constructor() {
        this.icons = {};
        this.reverseIcons = {};
        this.$panel = null;
        this.emojiClickedCallback = null; 
        this.emojiSource = $('body').data('emoji-img-url');
    }
    /**
     * Adds event listeners for emoji selection.
     *
     * @param {Event} event - The event triggering the emoji selection.
     * @param {function} emojiClickedCallback - Callback function for handling the selected emoji.
     */
    addListener(event, emojiClickedCallback) {
        if(this.$panel == null){
            this.emojiPanel();
        }
        this.setContainerPos(event);

        this.emojiClickedCallback = emojiClickedCallback;
        const KEY_ESC = 27;
        const KEY_TAB = 9;

        const $body = $('body');
        const self = this;

        $body.on('keydown', function (e) {
            if (e.keyCode === KEY_ESC || e.keyCode === KEY_TAB) {
                self.$panel.hide();
            }
        });


        $body.on('click', `.emoji-menu .emoji-menu-tab`, function (e) {
            e.stopPropagation();
            e.preventDefault();
            let index = 0;
            let curclass = $(this).attr("class").split(' ');

            curclass = curclass[1].split('-');
            if (curclass.length === 3) return;

            curclass = curclass[0] + '-' + curclass[1];
            
            $(`.emoji-menu .emoji-menu-tabs td`).each(function (i) {
                const $a = $(this).find('a');
                let aclass = $a.attr("class").split(' ');

                aclass = aclass[1].split('-');
                aclass = aclass[0] + '-' + aclass[1];

                if (curclass === aclass) {
                    $a.attr('class', 'emoji-menu-tab ' + aclass + '-selected');
                    if(i<6)
                    index = i;
                } else {
                    $a.attr('class', 'emoji-menu-tab ' + aclass);
                }
            });
            self.updateEmojisList(index);
        });
        $(document).off('click', `.emoji-menu .emoji-items a`);
        
        $(document).on('click', `.close-modal`, function () {
            self.$panel.hide();
        });

        $(document).on('click', `.emoji-menu .emoji-items a`, function () {
            const emoji = $('.label', $(this)).text();
            const $img = $(self.createdEmojiIcon(self.icons[emoji]));

            if ($img[0].attachEvent) {
                $img[0].attachEvent('onresizestart', function (e) {
                    e.returnValue = false;
                }, false);
            }
            
            if (self.emojiClickedCallback) {
                self.emojiClickedCallback($img[0]);
            }
            self.$panel.hide();


            ConfigStorage.get('emojis_recent', function (curEmojis) {
                curEmojis = curEmojis || Config.defaultRecentEmojis || [];
                const pos = curEmojis.indexOf(emoji);

                if (!pos) {
                    return false;
                }

                if (pos !== -1) {
                    curEmojis.splice(pos, 1);
                }

                curEmojis.unshift(emoji);

                if (curEmojis.length > 42) {
                    curEmojis = curEmojis.slice(42);
                }

                ConfigStorage.set({
                    emojis_recent: curEmojis
                });
            });
        });
    }
    /**
    * Loads emoji data into the class.
    */
    loadEmojis() {
        let icons = {};
        let reverseIcons = {};

        for (let j = 0; j < Config.EmojiCategories.length; j++) {
            const totalColumns = Config.EmojiCategorySpritesheetDimens[j][1];
            for (let i = 0; i < Config.EmojiCategories[j].length; i++) {
                const dataItem = Config.Emoji[Config.EmojiCategories[j][i]];
                const name = dataItem[1][0];
                const row = Math.floor(i / totalColumns);
                const column = i % totalColumns;
                icons[':' + name + ':'] = [j, row, column, ':' + name + ':'];
                reverseIcons[name] = dataItem[0];
            }
        }

        this.icons = icons;
        this.reverseIcons = reverseIcons;

        if (!Config.rx_codes) {
            Config.init_unified();
        }
    }
    /**
     * Sets the position of the emoji panel based on the event.
     *
     * @param {Event} event - The event triggering the emoji panel display.
     */
    setContainerPos(event){
        const emojiMenu = $('.emoji-menu-container');
        let offsetY = emojiMenu.height() /2 ;
        let topPosition = event.clientY - offsetY;
        const windowHeight = $(window).height();

        // Check if there is enough space below the event, otherwise, position above
        if (event.clientY + offsetY > windowHeight) {
            topPosition = event.clientY - emojiMenu.height() -50;
        }else if(event.clientY - emojiMenu.height() < 0){
            topPosition = event.clientY - 10 ;
        }

        emojiMenu.css({
        top: topPosition,
        left: event.clientX +10
        });
    }

    /**
     * Updates the list of emojis in the panel based on the selected category.
     *
     * @param {number} index - The index of the selected emoji category.
     */
    updateEmojisList(index) {
        const $items = $(`.emoji-menu .emoji-items`);
        $items.html('');

        if (index > 0) {
            $.each(this.icons, (key, icon) => {     
                if (this.icons.hasOwnProperty(key) && icon[0] === (index - 1)) {
                    $items.append('<a href="javascript:void(0)" title="' +
                        Config.htmlEntities(key) + '">' +
                        this.createdEmojiIcon(icon, true) +
                        '<span class="label">' + Config.htmlEntities(key) +
                        '</span></a>');
                }
            });
        } else {
            ConfigStorage.get('emojis_recent', (curEmojis) => {
                curEmojis = curEmojis || Config.defaultRecentEmojis || [];

                for (let i = 0; i < curEmojis.length; i++) {
                    const key = curEmojis[i];

                    if (this.icons[key]) {
                        $items.append('<a href="javascript:void(0)" title="' +
                            Config.htmlEntities(key) + '">' +
                            this.createdEmojiIcon(this.icons[key], true) +
                            '<span class="label">' + Config.htmlEntities(key) +
                            '</span></a>');
                    }
                }
            });
        }
    }
    /**
     * Creates HTML for displaying an emoji icon.
     *
     * @param {Array} emoji - Array containing emoji information.
     * @returns {string} - HTML representation of the emoji icon.
     */
    createdEmojiIcon(emoji) {
        const category = emoji[0];
        const row = emoji[1];
        const column = emoji[2];
        const name = emoji[3];
        const filename = this.emojiSource + '/emoji_spritesheet_!.png';
        const blankGifPath = this.emojiSource + '/blank.gif';
        const iconSize = 25;
        const xoffset = -(iconSize * column);
        const yoffset = -(iconSize * row);
        const scaledWidth = (Config.EmojiCategorySpritesheetDimens[category][1] * iconSize);
        const scaledHeight = (Config.EmojiCategorySpritesheetDimens[category][0] * iconSize);

        let style = 'display:inline-block;';
        style += 'width:' + iconSize + 'px;';
        style += 'height:' + iconSize + 'px;';
        style += 'background:url(\'' + filename.replace('!', category) + '\') ' +
            xoffset + 'px ' + yoffset + 'px no-repeat;';
        style += 'background-size:' + scaledWidth + 'px ' + scaledHeight + 'px;';

        return '<img src="' + blankGifPath + '" class="img" style="' +
            style + '" alt="' + Config.htmlEntities(name) + '">';
    }

    /**
     * Converts colon-based emoji notation to Unicode.
     *
     * @param {string} emoji - Emoji notation using colons.
     * @returns {string} - Unicode representation of the emoji.
     */
    colonToUnicode(emoij) {
        return emoij.replace(Config.rx_colons, (m) => {
            const val = Config.mapcolon[m];

            if (val) {
                return val;
            } else {
                return '';
            }
        });
    }

    /**
     * Initializes and displays the emoji panel.
    */
    emojiPanel() {
        this.$panel = $(`<div class="emoji-menu emoji-menu-container">\n` +
            '    <div class="emoji-items-wrap1">\n' +
            '        <table class="emoji-menu-tabs">\n' +
            '            <tbody>\n' +
            '            <tr>\n' +
            '                <td><a class="emoji-menu-tab icon-recent-selected"></a></td>\n' +
            '                <td><a class="emoji-menu-tab icon-smile"></a></td>\n' +
            '                <td><a class="emoji-menu-tab icon-flower"></a></td>\n' +
            '                <td><a class="emoji-menu-tab icon-bell"></a></td>\n' +
            '                <td><a class="emoji-menu-tab icon-car"></a></td>\n' +
            '                <td><a class="emoji-menu-tab icon-grid"></a></td>\n' +
            '            </tr>\n' +
            '            </tbody>\n' +
            '        </table>\n' +
            '        <div class="emoji-items-wrap mobile_scrollable_wrap">\n' +
            '            <div class="emoji-items"></div>\n' +
            '        </div>\n' +
            '    </div>\n' +
            '</div>'+
            '<div class="close-modal hide-modal"></div>').hide();
        this.$panel.appendTo('body');
        this.loadEmojis();
        this.updateEmojisList(0);
    }
    /**
     * Destroys the emoji picker, removing its elements from the DOM.
     */
    destroy() {
        this.$panel.remove();
        this.$panel = null;
    }
}
