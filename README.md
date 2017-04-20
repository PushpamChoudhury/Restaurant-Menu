# Restaurant-Menu
Restaurant-Menu provides a web application for managing restaurants i.e., user can perform [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operations to manage a list of restaurants. Alongwith restaurants, multiple menu items for each restaurants can also be managed.

It is based of [Flask](http://flask.pocoo.org/) framework. This application has user session management capability which is achieved using [Flask-Login](https://flask-login.readthedocs.io/en/latest/) package. In this application, SQLite3 is used as the database engine and in order to interact with the database in a object oriented way, SQLAlchemy is used as the Object Relational Mapper ([ORM](https://en.wikipedia.org/wiki/Object-relational_mapping)).

## Installation
For setup, install following extensions with pip:
```sh
$ pip install Flask
$ pip install flask-login
```
To install SQLite3 database, down precompiled binaries from [here](https://www.sqlite.org/download.html).

To download SQLAlchemy, click [here](https://www.sqlalchemy.org/download.html).

## Getting Started
Once installed, clone or download the project into your computer. Go into the ```src/``` directory and run the python files in it:
```sh
$ cd src/
$ python database_setup.py
$ python flask_server.py
```
The first program creates the necessary database tables and after successful execution, ```restaurantmenu.db``` database file should be created in the same directory.

The second program includes all the APIs for the application. After executing, it runs the application on ``` http://0.0.0.0:5000/ ```, so that the server is publicly available.

Finally, launch the application on ```http://localhost:5000``` or if you are accessing it from another computer on the network, then on ```http://[dev-host-ip]:5000```.

## Usage
In the home screen, there is a link to __*log in*__ which redirects user to login page. For all new users, user must register first, before being able to login. To register, user must click on __*New User Registration*__ link at the bottom of login page, which redirects user to registration page.

In the registration page, user must enter a username and password and click on ```Submit```, which creates a new user in the database and redirects the user to the login page. Now, the user can enter user details to access the application. On success, a user session is created which is closed when the user logs out of the application.
