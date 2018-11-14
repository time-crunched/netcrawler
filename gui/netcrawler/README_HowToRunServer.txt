To start the server you must first install the necassary java packages (nvd3.js and d3.js). This is done by giving the following command in the manage.py-folder:

"python manage.py bower_install"

And then you give the command:

"python manage.py collectstatic"

To start the server:

"python manage.py runserver"

The site should now be accessible on in your default browser: "http://127.0.0.1:8000/index"