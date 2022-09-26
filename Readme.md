
## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/setu-023/product-recommendation-system.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Then run these commands:

```sh
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```

Use this command to create superuser

```sh
(env)$ python manage.py createsuperuser
```

Once `pip` has finished downloading the dependencies:

```sh
(env)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.

openweathermap API KEY: `82a0819c96f416ad31782a78f046d871`
