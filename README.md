Outsource Factor
======================

**A Django application for building outsourcing sites.**

Overview
======================

This is a full fledged project that powers outsourcefactor.com.

Notice
======================
Outsourcefactor uses Django < 1.5, hence it ONLY works with Python 2.

How to use (DEVELOPMENT)
======================
```
$ python -m venv myenv
$ cd myenv
$ source bin/activate
$ pip install --upgrade pip
$ git clone https://github.com/un33k/oursourcefactor.git
$ cd outsourcefactor
$ git checkout development
$ cp private.py.example private.py
$ pip install -r env/dev/reqs.txt
$ bin/manage.py migrate
$ bin/manage.py runserver 0.0.0.0:8181
```
**Note:**
1. Modify private.py as per your development requirements
2. Modify social.py as per your requirements

How to use (PRODUCTION)
======================
```
$ python -m venv myenv
$ cd myenv
$ source bin/activate
$ pip install --upgrade pip
$ git clone https://github.com/un33k/outsourcefactor.git
$ cd outsourcefactor
$ git checkout production
$ cp private.py.example private.py
$ pip install -r env/prod/reqs.txt
$ bin/manage.py migrate
$ bin/manage.py collectstatic
```
**Note:**
1. Modify private.py as per your development requirements
2. Modify social.py as per your requirements
3. The `collectstatic` stores the static artifacts in `assets/collect` by default
5. Use `www/wsgi.py` with your production webserver

License
====================

Released under a ([MIT](LICENSE)) license.

