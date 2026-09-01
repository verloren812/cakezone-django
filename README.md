# CakeZone — Django project

The project is built on top of the `cakezone_class` HTML template.

## Structure

```
cakezone/
├── manage.py
├── cakezone/          # project settings: settings.py, urls.py, wsgi.py, asgi.py
├── templates/
│   ├── index.html     # base template: header, navigation, footer, styles and scripts
│   └── base.html      # the same template under the usual name: {% extends "index.html" %}
├── static/            # css, js, images, lib, scss
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

There is one relation between the models: `Dish.category` → `Category`
(`related_name="dishes"`), deleting a category deletes its dishes (`on_delete=CASCADE`).

## Static files and media

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]   # css/, js/, images/, lib/, scss/

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"            # chef and dish photos
```

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

## Admin site

All models are registered in the `admin.py` of their applications with `list_display`,
`list_filter` and `search_fields`; the category slug is filled automatically
(`prepopulated_fields`). The panel titles are set in `cakezone/urls.py`.

Superuser for the review: **admin / admin12345** (the `/admin/` address).
To create your own: `python manage.py createsuperuser`.

## How to run

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
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
into `media/`, so `MEDIA_ROOT` / `MEDIA_URL` can be seen in action.

The repository already contains the `0001_initial` migrations of all five applications
and the prepared `db.sqlite3` database.
