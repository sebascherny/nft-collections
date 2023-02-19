# NFT Custom Collection Project - Sebastian Cherny

Here is an explanation for setting up and running the project locally.

### Database

To run the project locally, you will need the SQL database set up. For that you have 2 options:

+ SQLITE: You can use SQLite for the database. This is much easier to install locally, but has many issues and is not recommended for a production environment.
If you want to go with this option, for now nothing else is necessary.

+ PostgreSQL: You can use PostgreSQL for the database, which is a good and scalable idea, but needs some more setup. If you want to go with this option, follow the steps below.

+ Go to https://postgresapp.com/

+ Download dmg file

+ Install the file in Applications and run it

After that, you can create a database. To create it from scratch:
### LINUX:
```sudo su postgres```
```postgres$ psql```

If database exists and you want to reset it:

```drop database nft_collections_db ;```

To create it:

```create database nft_collections_db;```

### MAC:

After launching the App, click on the postgres file that will open a postgresql terminal, and just type:

```postgres=# create database nft_collections_db;```

## Running

Open a terminal and move to the project parent folder. From there:

First we setup the virtual environment so that there are no libraries or versions problems and this steps work for every system:

Assuming you have python3 installed

```python3 -m pip install --user virtualenv```

```python3 -m venv env```

```source env/bin/activate```

```python3 -m pip install -r requirements.txt```

```export SECRET_KEY="AnyKeyForDjango"```

Now, depending on which database you want to use:

For Postgres, assuming nft_collection is database name:

```export DATABASE_URL=postgresql://localhost/nft_collection```

For sqlite:

```export USE_SQLITE=1```

```python3 src/manage.py migrate```

```python3 src/manage.py runserver```

It should be running!

You should see as output in the terminal the link where the server is running, which will most probably be http://127.0.0.1:8000/ . Go to that link and check you are in the login page.

Click on register (http://127.0.0.1:8000/register) and create a user.
After this you will already be able to create you first Custom Collection.

To create an admin user, run:

```python3 src/manage.py createsuperuser```

With that admin user you can go to http://127.0.0.1:8000/admin and see database objects.



### Testing

The API can be tested by going to the src/app/test folder and running:

```python3 ../../manage.py test```

Every test should pass. These are unittests that check that every API link works as expected for different parameters and situations, creating the appropriate changes in a test database.

Tests for the frontend (e.g. simulating clicks on the page) can be implemented for example with Jest but they are currently missing.

## Generic explanation of the code

* manage.py is the Django file that we will run to start our service. Should never be modified.

* settings.py defines all the settings, like the lifetime of the tokens for logged in users and the path for some folders.

* File urls.py defines which urls are known and reachable by the app. Here, links starting with 'api/' are urls to which we can do some of GET, POST, PUT, and will return valuable information with the result after the process. These links can be accessed by anyone with the corresponding permissions.
The other links are the frontend, the views.

* api.js is where all the calls to the 'api/...' links are done. It defines functions that will do the GET, POST, PUT to our backend API, and these functions are called from the other javascript files.

* external_api.js is where all the calls to the NFT Collections API are made.

* Other javascript files are the ones used for the frontend. They are imported in the corresponding .html files, which are themselves invoked when in the frontend we go to the links (the 'not api/ ' links).

### Database files

* migrations folder contains the structure of the database. Whenever we modify the database (add/edit/remove a field from a table, for example), after running the makemigrations command as explained above, a new .py file is created in this folder automatically, reflecting the database modification.

* models.py has the database structure, defining each table as a class (models.Model) with its corresponding fields and field types.

### Folder organization

* all_views: Here we have a file for each different type of object in our database. We define here the GET, POST, PUT, DELETE functions that are invoked when a 'api/...' link is called.
* static: Here we have all the css and javascript files
* templates: All the .html files invoked for each 'not api/...' view.


## API

We have a backend API that allows the user creation, and collections creation/edition/deletion.

* api/token/ : Receives a username and a password and returns, among other data, the token necessary to validate the identity.

* api/register/ : Receives username, email and password and, if username and email are unique, returns the user data as in api/token so that the user knows how to validate their identity.

* api/collections/ :
  - GET: Returns a list of a user's Custom Collections. Requires token authentication.
  - POST: Creates a new collection for the authenticated user. Receives fields collectionName that must be string, and tokensList that must be a list of {tokenId, image, name}

* api/collections/<int:collection_id>/ :
  - GET: Returns the collection information. Requires token authentication.
  - PUT: Edits the collection. Requires token authentication.
  - DELETE: Deletes the collection. Requires token authentication.
