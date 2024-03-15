# Connectr - Group Chat App

<img src="docs/read-me-images/mock-up.png" ><br>

![GitHub last commit](https://img.shields.io/github/last-commit/jamie33O/Code-Innovate-Chat-Hub?color=red)
![GitHub contributors](https://img.shields.io/github/contributors/jamie33O/Code-Innovate-Chat-Hub?color=orange)
![GitHub language count](https://img.shields.io/github/languages/count/jamie33O/Code-Innovate-Chat-Hub?color=yellow)
![GitHub top language](https://img.shields.io/github/languages/top/jamie33O/Code-Innovate-Chat-Hub?color=green)

<hr>

## Table of contents

- [Connectr - Group Chat App](#code-innovate-chat-hub---group-chat-app)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
  - [UX](#ux)
    - [Strategy](#strategy)
    - [Scope](#scope)
    - [Structure](#structure)
    - [Skeleton](#skeleton)
    - [Surface](#surface)
      - [Colour Scheme](#colour-scheme)
      - [Fonts](#fonts)
      - [Visual Effects](#visual-effects)
  - [Agile Methodology](#agile-methodology)
  - [Features](#features)
    - [Existing Features](#existing-features)
      - [Account pages](#account-pages)
      - [Group chat/Homepage](#group-chathomepage)
      - [Custom Error pages](#custom-error-pages)
      - [Messaging](#messaging)
      - [Profile Page](#profile-page)
      - [Header Navigation section](#header-navigation-section)
      - [Emoji modal](#emoji-modal)
    - [Future Feature Considerations](#future-feature-considerations)
  - [Responsive Layout and Design](#responsive-layout-and-design)
  - [Tools Used](#tools-used)
    - [Python packages](#python-packages)
  - [Testing](#testing)
  - [Deployment](#deployment)
    - [Deploy on Heroku](#deploy-on-heroku)
    - [Code](#code)
  - [Acknowledgements](#acknowledgements)

## Overview

The Connectr is a Django-based web application designed for a coding course community. The home page features group chat functionality, allowing users to participate in discussions related to the Code Innovate coding course. Users can create and join different chat channels, engaging in real-time conversations with fellow learners. The Direct Message section enables one-on-one communication, allowing users to connect and share information privately. Additionally, each user has a Profile Page for managing account settings, viewing activity, and accessing joined chat channels. The application prioritizes real-time updates, supports multimedia content, and incorporates authentication and authorization features for secure user interactions. The Connectr aims to foster collaborative learning and communication within the coding community, offering a platform akin to popular communication tools like Slack.
<br><br>
The fully deployed project can be accessed here [Connectr](https://ci-chathub-f163e2297a1b.herokuapp.com/).
<br><br>

## UX

This site was created respecting the Five Plans Of Website Design:<br>

### Strategy<hr>

**Project Goal:**<br>
Create a website similar to Slack but specifically tailored for Code Innovate.

**Project Objectives:**<br>

- Develop a real-time messaging platform to facilitate seamless communication among Connectr community members.
- Implement a user-friendly interface with channels dedicated to various Connectr topics, fostering organized discussions.
- Enhance user engagement with multimedia support in direct messages and emoji reactions for interactive conversations.
- Establish secure user authentication, authorization, and profile management features to ensure a personalized and protected user experience.
  <br><br>

### Scope<hr>

**User Management**

- User registration and authentication.
- User roles and permissions for various levels of access.
- Profile creation and management.

**Communication Features**

- Real-time messaging functionality for group discussions in channels.
- Direct messaging for private one-on-one conversations.
- Multimedia support, including file attachments and emoji reactions.

**Channel Management**

- Creation, joining, and leaving of channels.
- Categorization of channels based on Code Innovate topics or modules.
- Ability to search and discover relevant channels.

**User Interface and Experience**

- Intuitive and user-friendly interface for seamless navigation.
- Responsive design for accessibility on various devices.
- Personalization options for user profiles.

**Responsiveness**<br>

- Create a responsive design for desktop, tablet and mobile devices.<br><br>

### Structure<hr>

The structure of the website is divided into seven pages but with content depending on authentication and client/staff status <br>

- **Register/Login/logout/email settings/password change** for this the Django app Allauth was used, the pages give the user the possibility to create an account, login or log out, add or remove emails and change there password.<br>

- The **Home** page consists of 3 sections channels/unread messages list, posts and comments.Posts and comments are loaded using ajax depending on the link the user clicks<br>

- The **header** is visible on all pages on large screens and only on main pages e.g home,messages,profile on mobile it consists of a search bar and a settings icon <br>

- The **header menu** consists of five links if the user is a staff member or four otherwise and it is only visible if the user is logged in
  - _Add Channel_ \*Only shows if the user is a staff member
  - _Logout_
  - _Change Password_
  - _Email Settings_
  - _Delete Account_
- The **Header Search bar** is used to find another user or find a specific channel the user is asked to type the @ symbol for users list or # for channels
- The **Admin panel** page is only available for staff members, here they can approve users also add channels or remove posts or comments <br>

- **Messages** contains an inbox with a search bar to search for a specific conversation and then the direct private messages list between users<br>

- The **Profile** page consists of three sections the users profile view which can be viewed by other user when they click on that users profile picture in anywhere trough the site, the edit profile section and the saved posts section <br>

### Skeleton<hr>

**Wireframes**<br>
The wireframes for mobile and desktop were created with [Balsamiq]() tool and can be viewed [here]()<br>

<details>
  <summary>Wire Frames</summary>
  <h4>Channels list</h4>
  <img src="docs/read-me-images/wireframes/home-tab.png"><br>
  <h4>Delete account modal</h4>
  <img src="docs/read-me-images/wireframes/delete-account.png"><br>
  <h4>Edit Profile</h4>
  <img src="docs/read-me-images/wireframes/edit-profile-page.png"><br>
  <h4>Login page</h4>
  <img src="docs/read-me-images/wireframes/login-page.png"><br>
  <h4>Logout page</h4>
  <img src="docs/read-me-images/wireframes/logout.png"><br>
  <h4>Comment's</h4>
  <img src="docs/read-me-images/wireframes/message-comment-in-channel-page.png"><br>
  <h4>Messages</h4>
  <img src="docs/read-me-images/wireframes/messages-page.png"><br>
  <h4>Inbox</h4>
  <img src="docs/read-me-images/wireframes/messages-tab.png"><br>
  <h4>View profile</h4>
  <img src="docs/read-me-images/wireframes/profile-tab.png"><br>
  <h4>Sign up page</h4>
  <img src="docs/read-me-images/wireframes/register-page.png"><br>
  <h4>Header menu drop-down</h4>
  <img src="docs/read-me-images/wireframes/settings-drop-down.png"><br>
</details>
</details><br>

**FLOWCHARTS**<br>
The Flowchart for my program was created using <b>[draw.io](https://app.diagrams.net/)</b> and it visually represents how the system works.<br>
<img src="docs/read-me-images/flowchart/flow-chart-ci-chathub.jpg.drawio.png"><br>
<br><br>

**Database**<br>
The project uses the PostgreSQL relational database for storing the data.<br>
There was two diagrams created to represent the relation between the tables, the initial one and the final one.
The first one was created before the actual development of the website which led to some changes to the attributes and tables for finding the most relevant and useful ones to be kept.

<details>
  <summary>Initial Schema</summary>
<img src="docs/read-me-images/database-diagrams/database_diagram.png" ><br>
</details>

<details>
  <summary>Final Schema</summary>
    <h4>Group chat app</h4>
    <img src="docs/read-me-images/database-diagrams/group_chat_app.png"><br>
    <h4>Messaging</h4>
    <img src="docs/read-me-images/database-diagrams/messagng.png"><br>
    <h4>User Profile</h4>
    <img src="docs/read-me-images/database-diagrams/user_profile.png"><br>
</details><br>

### Surface<hr>

#### Colour Scheme

- The primary colour scheme was used for body, headers and nav elements<br>
  <img src="docs/read-me-images/color-scheme/clr1.jpg" width="30%">
  <img src="docs/read-me-images/color-scheme/clr2.png" width="30%">
  <img src="docs/read-me-images/color-scheme/clr3.jpeg" width="30%">
  <img src="docs/read-me-images/color-scheme/clr4.png" width="30%">
  <img src="docs/read-me-images/color-scheme/clr5.png" width="30%">
  <br>

- The secondary colour scheme was used for buttons, warnings, errors or for highlighting important information.<br>
  <img src="docs/read-me-images/color-scheme/clr6.png" width="30%">
  <img src="docs/read-me-images/color-scheme/clr7.png" width="30%">
  <img src="docs/read-me-images/color-scheme/clr8.png" width="30%">
  <img src="docs/read-me-images/color-scheme/clr9.png" width="30%">

#### Fonts

- The fonts I used for this site were imported from [Google Fonts](https://fonts.google.com/):<br>
  **H tags:** _EB Garamond, serif_<br>
  **body:** _Roboto, serif_<br>

#### Visual Effects

- **Box shadows** <br>
  Multiple box shadows were used for the cover, buttons and images. <br>
- **Animation**<br>
Some animations were used for creating a dynamic and attractive design
<details>
  <summary>Displaying notifications</summary>
<img src="docs/read-me-images/animations/notification1.png">
<img src="docs/read-me-images/animations/notification.png"><br>
</details>
<details>
  <summary>Search bar</summary>
<img src="docs/read-me-images/animations/search-bar.png">
<img src="docs/read-me-images/animations/search-bar1.png"><br>
</details>

## Agile Methodology

This project was developed using the Agile methodology.<br>
All epics and user stories implementation progress was registered using [Github issues](https://github.com/jamie33o/pp4/issues). As the user stories were accomplished, they were moved in the Kanban Board from **Epic**,**User stories**, **To Do**, to **In-progress**, **Testing** and **Done** lists.

<details>
<summary>Sprints Details</summary>
 
* **Sprint 1 - Epic #1**<br>
  - Epic: #1 Create login and register page<br>
  - complete the user stories for this epic <br>
* **Sprint 2 - Epic #2**<br>
  - Epic #2: Create a direct messaging page<br>
  - complete the user stories for this epic<br>
* **Sprint 3 - Epic #3**<br>
  - Epic #3: Create a Profile page<br>
  - complete the user stories for this epic<br>
* **Sprint 4 - Epic #4**<br>
  - Epic #4: Create a Group chat homepage<br>
  - complete the user stories for this epic<br>
</details><br><br>

## Features

### Existing Features<hr>

#### Account pages

Our website leverages the Django Allauth package for streamlined user authentication and registration. With Allauth, users can easily register using email confirmation. The package provides a secure and customizable solution, offering features such as password reset, email verification, and user-friendly account management views. We chose Allauth for its flexibility, robustness, and the ability to tailor the authentication process to our site's unique needs, ensuring a seamless and secure experience for our users.

- Sign in page<br><br>
  <img src="docs/read-me-images/sign-in.png" width="60%"><br><br>
- Sign up page<br><br>
  <img src="docs/read-me-images/sign-up.png" width="60%"><br><br>
- Sign out page<br><br>
  <img src="docs/read-me-images/sign-out.png" width="60%"><br><br>
- Email settings page<br><br>
  <img src="docs/read-me-images/email-settings.png" width="60%"><br><br>
- Change Password page<br><br>
  <img src="docs/read-me-images/change-password.png" width="60%"><br><br>

#### Group chat/Homepage

- On the group chat homepage the page is divided into three sections.

  1. The channels/New messages list <br><br>
     - The channels can be added by staff members and will appear in this list, it shows a count of the amount of members of the specific channel
     - The New messages list is populated when the user has unread messages <br><br>
       <img src="docs/read-me-images/channels-new-messages-list.png" width="60%"><br><br>
  2. The posts for the channel the user has chosen to view <br><br>
     <img src="docs/read-me-images/posts-list.png" width="60%"><br><br>
  3. comments on a specific post, the comments section only shows when the user clicks the comments link on any given post and the post the user clicks is brought into the comment section and comments can then be posted underneath it<br>

  - Comments visible<br><br>
    <img src="docs/read-me-images/group-chat-with-comments.png" width="60%"><br><br>
  - Comments hidden<br><br>
    <img src="docs/read-me-images/group-chat-homepage.png" width="60%"><br><br>
    <br>
    <img src="docs/read-me-images/comments-list-commetns.png" width="60%"><br><br>

- Both the posts section and the comments section have an editor, Summer-note editor was used for this it was enhanced to also have emoji's and tagging functionality.

#### Custom Error pages

- 403 error page<br><br>
  <img src="docs/read-me-images/403.png" width="60%"><br><br>
- 404 error page<br><br>
  <img src="docs/read-me-images/404.png" width="60%"><br><br>
- 500 error page<br><br>
  <img src="docs/read-me-images/500.png" width="60%"><br><br>

#### Messaging

- On the _Messages_ page, users have an inbox displaying a comprehensive list of all their conversations with other users. Clicking a conversation link loads the messages list and editor using AJAX. The inbox is equipped with a search bar for users to easily navigate through their conversations.
  <br><br>
  <img src="docs/read-me-images/messaging.png" width="70%"><br><br>

#### Profile Page

The Profile page is divided into three sections:
<br><br>
<img src="docs/read-me-images/profile-tab-full.png" width="70%"><br><br>

1.  _Profile view_ section

- The Profile view section represents how other users perceive one's profile. The menu is only visible to the current user and can be accessed by clicking their profile picture on posts, comments, or messages.<br>
  <br>
- This is the profile view the user can see if they click the profile tab<br><br>
  <img src="docs/read-me-images/view-profile-from-tab.png" width="70%"><br><br>
- This is the view when a user clicks another user's profile picture<br><br>
  <img src="docs/read-me-images/view-profile-modal-different-user.png" width="70%"><br><br>

- The menu in the profile view has 3 links the first is for the user to change there profile picture when clicked a modal shows up where the user can change there profile image<br><br>
  <img src="docs/read-me-images/update-profile-pic-modal.png" width="70%"><br><br>

- The second link is for the user to update there status when clicked it a modal shows up where the user can change there status<br><br>
  <img src="docs/read-me-images/update-status-modal.png" width="70%"><br><br>

2. The _Edit profile_ section here the user can add there bio, website and social links <br><br>
   <img src="docs/read-me-images/edit-profile.png" width="70%"><br><br>

3. The third link is for displaying the list of saved posts<br><br>
   <img src="docs/read-me-images/saved-posts.png" width="70%"><br><br>

#### Header Navigation section

The Header section contains the settings icon, website name and the search bar<br>
<br>
<img src="docs/read-me-images/header-nav.png" width="100%"><br><br>
<br>

- Settings menu<br><br>
  <img src="docs/read-me-images/header-menu.png" width="40%"><br><br>
- Search bar list<br><br>
  <img src="docs/read-me-images/search-box.png" width="40%"><br><br>

#### Emoji modal

The Emoji model is used to add emoji's to posts, comments, messages and summernote editor<br>
<br>
<img src="docs/read-me-images/emoji-modal.png" width="40%"><br><br>
<br>

### Future Feature Considerations<hr>

- One possible feature would be the implementation of a _Points system_ with badges. Every time a user helps another user by answering a question or helping with a bug, they get points and when they get a certain amount of points they get a badge.

- Another feature would be video calls

## Responsive Layout and Design

The project design has been adapted to all types of devices using Bootstrap predefined breakpoints. For intermediate devices where the design didn't fit accordingly, custom breakpoints were used.

**Breakpoints:** - max-width:575.98px - max-width:991.98px - max-width:1300.98px

**Tested devices:**

    - Moto G4
    - iPhone SE
    - iPhone XR
    - iPhone 11
    - iPhone 13
    - iPhone 5/SE
    - iPhone 6/7/8
    - Ipad
    - Ipad Air
    - Ipad Mini
    - Ipad Pro
    - Pixel 5
    - Surface Duo
    - Surface Pro 7
    - Nest Hub
    - Nest Hub Max
    - Samsung Galaxy S20 Ultra
    - Samsung Galaxy S8
    - Galaxy Note 2
    - Galaxy Tab S4
    - Asus Vivobook

## Tools Used

[GitHub](https://github.com/) - used for hosting the source code of the program<br>
[Visual Studio](https://code.visualstudio.com/) - for writing and testing the code<br>
[Heroku](https://dashboard.heroku.com/) - used for deploying the project<br>
[Balsamiq](https://balsamiq.com/wireframes/) - for creating the wireframes<br>
[Draw.io](http://draw.io/) - used for creating the Flowchart and Database relational schema<br>
[Favicon.io](https://favicon.io/) - used for generating the website favicon<br>
[Font Awesome](https://fontawesome.com/) - for creating atractive UX with icons<br>
[Bootstrap5](https://getbootstrap.com/) - for adding predifined styled elements and creating responsiveness<br>
[Google Fonts](https://fonts.google.com/) - for typography<br>
[JsHint](https://jshint.com/) - used for validating the javascript code<br>
[PEP8 Validator](http://pep8online.com/) - used for validating the python code<br>
[HTML - W3C HTML Validator](https://validator.w3.org/#validate_by_uri+with_options) - used for validating the HTML<br>
[CSS - Jigsaw CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_uri) - used for validating the CSS<br>
[Chrome Del Tools](https://developer.chrome.com/docs/devtools/) - for debugging the project<br>
[W.A.V.E.](https://wave.webaim.org/) - for testing accessibility<br>
[ElephantSQL](https://www.elephantsql.com/) - for storing static data<br>
[Docker desktop](https://www.docker.com/products/docker-desktop/) - for testing the websockets locally<br>
LightHouse - for testing performance<br>

### Python packages

asgiref==3.7.2<br>
astroid==2.15.8<br>
attrs==23.1.0<br>
autobahn==23.6.2<br>
Automat==22.10.0<br>
bleach==3.3.1<br>
boto3==1.28.57<br>
botocore==1.31.57<br>
cachetools==5.3.1<br>
certifi==2023.7.22<br>
cffi==1.16.0<br>
channels==4.0.0<br>
channels-redis==4.1.0<br>
charset-normalizer==3.2.0<br>
constantly==15.1.0<br>
cryptography==41.0.4<br>
daphne==4.0.0<br>
defusedxml==0.7.1<br>
dill==0.3.7<br>
dj-database-url==2.1.0<br>
Django==3.2.21<br>
django-allauth==0.41.0<br>
django-crispy-forms==1.14.0<br>
django-emoji==2.2.2<br>
django-storages==1.14.1<br>
emoji==2.8.0<br>
gunicorn==21.2.0<br>
hyperlink==21.0.0<br>
idna==3.4<br>
incremental==22.10.0<br>
isort==5.12.0<br>
jmespath==1.0.1<br>
lazy-object-proxy==1.9.0<br>
mccabe==0.7.0<br>
msgpack==1.0.7<br>
oauthlib==3.2.2<br>
packaging==23.1<br>
Pillow==10.0.1<br>
platformdirs==3.10.0<br>
psycopg2==2.9.8<br>
pyasn1==0.5.0<br>
pyasn1-modules==0.3.0<br>
pycparser==2.21<br>
Pygments==2.16.1<br>
pylint==2.17.6<br>
pylint-django==2.5.3<br>
pylint-plugin-utils==0.8.2<br>
pyOpenSSL==23.2.0<br>
python-dateutil==2.8.2<br>
python3-openid==3.2.0<br>
pytz==2023.3.post1<br>
redis==5.0.1<br>
requests==2.31.0<br>
requests-oauthlib==1.3.1<br>
rsa==4.9<br>
s3transfer==0.7.0<br>
service-identity==23.1.0<br>
six==1.16.0<br>
sqlparse==0.4.4<br>
tomlkit==0.12.1<br>
txaio==23.1.1<br>
typing_extensions==4.8.0<br>
urllib3==1.26.16<br>
webencodings==0.5.1<br>
wrapt==1.15.0<br>
zope.interface==6.1<br>

## Testing

The testing documentation can be found at [TESTING.MD](TESTING.md)

## Deployment

### Deploy on Heroku

1.  Create Pipfile

In the terminal enter the command ` pip3 freeze > requirements.txt`, and a file with all requirements will be created.

2. Setting up Heroku

   - Go to the Heroku website (https://www.heroku.com/)
   - Login to Heroku and choose _Create App_
   - Click _New_ and _Create a new app_
   - Choose a name and select your location
   - Go to the _Resources_ tab
   - From the Resources list select _Heroku Postgres_
   - Navigate to the _Deploy_ tab
   - Click on _Connect to Github_ and search for your repository
   - Navigate to the _Settings_ tab
   - Reveal Config Vars and add your aws, Database URL and Secret key.

1. Deployment on Heroku

   - Go to the Deploy tab.
   - Choose the main branch for deploying and enable automatic deployment
   - Select manual deploy for building the App

## Credits

### Code

- The code for implementing the emoji modal was obtained from this [GitHub repository](https://github.com/trinhtam/summernote-emoji) . However, I have customized and refactored it to better align with the specific requirements of my website
- The code for channels app was got [here](https://channels.readthedocs.io/en/latest/)
- The html for the post card and the all auth card was inspired from [here](https://bootsnipp.com/)
- Django pagination was taken and adapted from [here](https://stackoverflow.com/questions/12275926/django-pagination)
- The summernote code was got form [here](https://summernote.org/) However, I have customized and refactored it to better align with the specific requirements of my website

- Slack community for great involvement in helping each other<br>
<hr>
