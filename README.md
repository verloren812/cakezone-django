# CakeZone — Django project

The project is built on top of the `cakezone_class` HTML template.

## Structure

```
cakezone/
├── manage.py
├── cakezone/          # project package: settings/, urls.py, wsgi.py, asgi.py
│   └── settings/      # base.py (common), dev.py (development), prod.py (production)
├── templates/
│   ├── index.html     # base template: header, navigation, footer, styles and scripts
│   └── base.html      # the same template under the usual name: {% extends "index.html" %}
├── static/            # css, js, images, lib
├── media/             # uploaded files: chef and dish photos
├── main/              # "Home" section          -> /
├── menu/              # "Menu & Pricing"        -> /menu/
├── team/              # "Master Chefs"          -> /team/
├── service/           # "Our Service"           -> /service/
└── contact/           # "Contact Us"            -> /contact/
```

Every application has its own `views.py`, `urls.py` (with `app_name`) and a page template:

| Page | Template |
|---|---|
| Home | `main/templates/main/home.html` |
| Menu & Pricing | `menu/templates/menu/menu_pricing.html` |
| Master Chefs | `team/templates/team/master_chefs.html` |
| Our Service | `service/templates/service/our_service.html` |
| Contact Us | `contact/templates/contact/contact_us.html` |

All of them start with `{% extends "base.html" %}` and fill the `{% block title %}`
and `{% block content %}` blocks of the base template.

## Routes

| URL | Application | View |
|---|---|---|
| `/` | main | `index` |
| `/menu/` | menu | `index` |
| `/menu/<category>/` | menu | `category` (a route built with `re_path`) |
| `/team/` | team | `index` |
| `/service/` | service | `index` |
| `/contact/` | contact | `index` |
| `/admin/` | django.contrib.admin | — |

The category route is built with a regular expression:

```python
re_path(r"^(?P<category>[a-z][a-z-]{2,20})/$", views.category, name="category")
```

## Models

| Application | Model | Purpose |
|---|---|---|
| main | `Establishment` | information about the bakery: description, photo, counters |
| main | `Testimonial` | client testimonials: author, profession, text, photo, rating |
| menu | `Category` | dish categories (Birthday / Wedding / Custom), the slug is used in the route |
| menu | `Dish` | dishes: name, description, price, weight, photo, `ForeignKey` to the category |
| team | `Chef` | chefs: name, designation, photo, biography, experience, social links |
| service | `Service` | services: title, description, icon, price from |
| contact | `ContactInfo` | contacts: address, email, phone, working hours, social links, map code |
| contact | `ContactMessage` | a message from the form: name, email, subject, text, received at, processed |

There is one relation between the models: `Dish.category` → `Category`
(`related_name="dishes"`), deleting a category deletes its dishes (`on_delete=CASCADE`).

## Static files and media

```python
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]   # css/, js/, images/, lib/
STATIC_ROOT = BASE_DIR / "staticfiles"     # target of collectstatic (not committed)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"            # chef and dish photos
```

In production run `python manage.py collectstatic` and let the web server (nginx)
serve `staticfiles/` at `/static/` and `media/` at `/media/`: Django serves media only
when `DEBUG = True`.

Static files are linked with the `{% static %}` tag:

```django
{% load static %}
<link href="{% static 'css/style.css' %}" rel="stylesheet">
<script src="{% static 'js/main.js' %}"></script>
<img src="{% static 'images/cake-1.jpg' %}" alt="">
```

In debug mode the media files are served by this line in `cakezone/urls.py`:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Context processor

`main/context_processors.py` → `site_context()` is registered in `settings.TEMPLATES`
and provides to **every** page:

* `site` — the active `Establishment` record (the name in the header, the description in the footer);
* `contacts` — the active `ContactInfo` record (email and phone in the topbar, address and social links in the footer);
* `menu_categories` — the menu categories.

Because of that the header and the footer of `templates/index.html` are filled from the
database instead of being hardcoded in the markup. The labels themselves are wrapped in
`{% trans %}`, so the site is ready for translation.

## Feedback form

The Contact Us page carries a working form: a visitor writes a message, it is validated on
the server and stored in the database.

| File | Role |
|---|---|
| `contact/models.py` | `ContactMessage` — the stored message |
| `contact/forms.py` | `ContactMessageForm` — a `ModelForm` over that model, with the Bootstrap widgets of the template |
| `contact/views.py` | `index` — serves both the GET and the POST of the same address |
| `contact/templates/contact/contact_us.html` | renders the fields, their errors and the confirmation |
| `contact/admin.py` | `ContactMessageAdmin` — the received messages, read-only |

Validation happens in three layers: the field types of the model (the name is required, the
address must be a valid email), the `max_length` of the columns, and `clean_message()` in
the form, which rejects messages shorter than 10 characters.

After a successful save the view answers with a redirect instead of a page
(**Post/Redirect/Get**), so pressing F5 no longer offers to send the data once more. The
confirmation survives the redirect through `django.contrib.messages` and is shown exactly
once. The form itself is protected by `{% csrf_token %}`.

In the admin site the text and the address of the sender are `readonly_fields`: a received
message must not be edited, only marked as processed.

## Admin site

All models are registered in the `admin.py` of their applications with `list_display`,
`list_filter` and `search_fields`; the category slug is filled automatically
(`prepopulated_fields`). The panel titles are set in `cakezone/urls.py`.

`python manage.py seed_demo` creates a demo administrator for the local database:
**admin / admin12345** (the `/admin/` address). The prepared `db.sqlite3` of the repository
already contains it. For an account of your own: `python manage.py createsuperuser`.

## Settings and environment variables

The settings are split into a package:

| Module | Purpose | Used by default in |
|---|---|---|
| `cakezone/settings/base.py` | common settings, reads the environment and `.env` | — |
| `cakezone/settings/dev.py` | `DEBUG` on, hosts `localhost`, `127.0.0.1` | `manage.py` |
| `cakezone/settings/prod.py` | `DEBUG = False`, HTTPS and secure cookies, required key and hosts | `wsgi.py`, `asgi.py` |

Another module is chosen with the `DJANGO_SETTINGS_MODULE` environment variable.
No secrets are stored in the code: copy `.env.example` to `.env` (it is in `.gitignore`)
and fill in the values.

| Variable | dev | prod |
|---|---|---|
| `DJANGO_SECRET_KEY` | optional (without it a random key is generated on every start, so the admin login is reset on restart) | **required** |
| `DJANGO_DEBUG` | `true` by default | ignored, always `False` |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1]` by default | **required**, e.g. `cakezone.example.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | not needed | e.g. `https://cakezone.example.com` |
| `DJANGO_SECURE_SSL` | — | `true` by default; `false` to try prod settings without HTTPS |

A secret key is generated with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Production check:

```bash
DJANGO_SETTINGS_MODULE=cakezone.settings.prod python manage.py check --deploy
```

## How to run

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env       # Windows (cp on Linux/macOS), then set DJANGO_SECRET_KEY
python manage.py migrate
python manage.py runserver
```

The site opens at http://127.0.0.1:8000/

## Demo data

```bash
python manage.py seed_demo
```

The command (`main/management/commands/seed_demo.py`) clears the section tables and fills
them with examples: the establishment with counters, 4 testimonials, 3 categories with
7 cakes, 3 chefs, 3 services and the contacts. Images are copied from `static/images`
into `media/`, so `MEDIA_ROOT` / `MEDIA_URL` can be seen in action. The command also creates
the demo administrator described above, if it is missing.

The repository contains the migrations of all five applications (`contact` has a second one,
`0002_contactmessage`) and the prepared `db.sqlite3` database with the demo data and the demo
administrator.
