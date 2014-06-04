MySDS is a database for any institution working in the education sector (the name is a not-very-good pun on MySQL and an application in use at one of the Universities I worked at: SDS - Student Data System. If you have a better idea for a name, I am very, very open for suggestions!). Currently, all configuration is done for the Law Programmes at Canterbury Christ Church University, but I am planning to work on making it a general purpose application that can easily be adapted to suit your needs as well - whether you want to use it for a University department, a school, an FE college or anything else.

# Aims

This project has been started by a lecturer in law, who also happens to be an open source enthusiast and a hobby programmer ([more here](http://www.tobiaskliem.de)). In my dayjob I realised that almost every university seems to rely on horribly complicated proprietary database systems that were not designed with the teacher in mind. The aim of this system is to have an easy to use database application that relies on open standards and makes it very easy to get the data out in machine readable formats should the user want to switch after all. Currently, almost everything is exportable in pretty PDF files, but soon it should be easy to get your data in csv and json files as well, so that even a typical, non-technical teacher can save a backup they can open with Microsoft Excel or similar soul-destroying applications.

This application is not trying to be a huge Virtual Learning Environment that allows you to post slides, videos, upload assessments or let the students create Wikis. Instead, it is supposed to stay focused on its main goal - to make the teacher's life easier by automating repetetive tasks, offering a quick way to access records for modules and students and a simple solution to share assessment feedback and marks with the students.

# Installation

The database is based on [Django](http://www.djangoproject.org), a very versatile webframework based on Python. You will need the following dependencies:

* Python (version 2.x) and the Python-markdown package (available in most Linux distributions)
* [Django](http://www.djangoproject.org)
* Apache (or any other webserver you want to use, but I haven't tested with anything else)
* SQLite or any other database that works with Django, in case you want to use anything else, you need to adapt `mysds/settings.py`
* [Reportlab](http://www.reportlab.com/software/opensource/) for generating PDF files

Once you have all of that, get the repository, set up your initial database with `python manage.py syncdb` (if you are using a bleeding edge distro, you might have to type `python2 manage.py syncdb` instead), create a superuser during that process if you want to, and you are ready to go. You can start the testserver with `python manage.py runserver`, and you can access the website itself over `localhost:8000` and the Django admin interface over `localhost:8000/admin`.

By default, there already is a superuser set up, and you can access both the website itself and the admin interface with the username `admin` and the password `admin`. Don't forget to change the password or delete that user later!

If you want to use this in production, you will need to run `python manage.py collectstatic`, and to set up your webserver to display the website and to deliver the static files (CSS, Javascript, pictures etc). There are loads of guides on how to do configure whichever webserver you want to use with Django ([for example this one for Apache](https://docs.djangoproject.com/en/1.5/howto/deployment/wsgi/modwsgi/)).

This project is still a work in progress, so if you want to use it for production, make sure you have lots of backups...

# Outstanding Tasks

* TESTS, TESTS, TESTS!
* making the application easier to adapt for other institutions and programmes
* making sure the templates are mobile responsive, so that the application can be used on phones
* exporting data into machine-readable formats: csv, json, etc
* clean up my potentially awful (hobby programmer) coding style, ask me to add comments where you don't understand the functions etc

If you find any problems or bugs, or if you have any questions, use the issues form here or contact me at [tobi@tobiaskliem.de](mailto:tobi@tobiaskliem.de?subject=Mysds).
