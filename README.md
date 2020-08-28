# Bon Voyage

**A website like Airbnb, an online marketplace which lets people rent out their properties or spare rooms to guests and to book hotels and much more !**

Files and Directories:

- ``` travel ``` - main application directory.
    - ``` static/travel ``` -  contains all static content.
        - ``` styles.scss``` - source SCSS file.
        - ``` styles.css ``` - contains compiled CSS file.
        - ``` styles.css.map ``` - contains CSS map.
        - ``` index.js ``` - script that runs on Home page and Place page.
        - ``` icon.png, jumbo.jpg, user.png ``` - Image files.
    - ``` templates/ travel ``` - contains all application templates.
        - ``` layout.html ``` - A base template where all other tempalates extend it.(also a Standard Home page contains Pagination and more)
        - ``` host.html ``` - template for hosting a new place and this template is also rendered when editting the place.
        - ``` index.html ``` - template that allows the user to search for a place and gives its search results.
        - ``` login.html ``` - template to login a user.
        - ``` payment.html ``` - template to get the payment from the user when the user books a place.
        - ``` place.html ``` - template for showing all the details , images and more about the current place they are looking into.
        - ``` register.html ``` - template to rgister a new user.
    - ``` admin.py ``` - Added some admin classes and registered all the models.
    - ``` forms.py ``` - Contains two model forms from Place Model and Images model and combined into a one form.
    - ``` models.py ``` - Contains 6 models. User model inherited from Abstract user, Place model which contains all the places created by all the registered user, Images model to save the images of individual place, Customer model which contains all the users and the respective places they booked, Comment model that represent users comments and Save model that represent user's saved list.
    - ``` urls.py ``` - contains all application URLs.
    - ```views.py```- contains all application views.
- ``` finalproject ```- project directory .
- ```media ```- this directory contains all of the images that are saved in Images model.


You can watch the video representation of this project in [Bon Voyage](https://youtu.be/_vT9KK9ssao).