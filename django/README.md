# Django delivery quotes

A beginner Django project that turns delivery pricing into a web application.
Enter a parcel's weight, destination postcode, and delivery type to calculate and
save a quote. The main page lists previous quotes, newest first, and each quote
links to its own detail page.

## Setup and run

From the repository root:

```sh
cd django
```

Create the project's environment if `.venv` does not already exist:

```sh
python3 -m venv .venv
```

Activate it, install dependencies, apply database migrations, and start the server:

```sh
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. Stop the development server with **Ctrl + C**.
This server is for local development.

This project has its own environment, separate from the data analysis project.
In VS Code, open this `django` folder and select `.venv/bin/python` using
**Python: Select Interpreter**. Terminal activation and the editor's interpreter
selection are separate.

## Try the scenario

1. Enter a weight of 3 kg and a postcode such as `SW1A 1AA`.
2. Choose standard delivery and submit: the quote should be **£6.00**.
3. Choose express delivery for the same weight: it should be **£25.00**.
4. Find both records under **Previous quotes**.
5. Click a quote ID to open its detail page.
6. Try a negative weight: the form should show an error without saving a quote.

Standard pricing is £2 per kilogram. Express pricing is £5 per kilogram plus £10.
The postcode is stored but does not affect the price.

## Project and app structure

A Django **project** contains configuration for the site. An **app** groups a
feature's models, views, forms, and templates.

```text
django/
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py
│   └── urls.py
└── deliveries/
    ├── apps.py
    ├── urls.py
    ├── forms.py
    ├── pricing.py
    ├── models.py
    ├── admin.py
    ├── tests.py
    ├── migrations/
    │   └── 0001_initial.py
    ├── views/
    │   ├── __init__.py
    │   ├── home.py
    │   └── quote_detail.py
    └── templates/deliveries/
        ├── home.html
        └── quote_detail.html
```

`manage.py` runs project commands. `config/settings.py` registers the app as
`deliveries.apps.DeliveriesConfig` and configures SQLite. The database is stored
locally in `db.sqlite3`.

## URLs, views, and templates

| Request | Behaviour |
| --- | --- |
| `GET /` | Displays the form and all saved quotes |
| `POST /` | Validates input, calculates and saves a quote, then redirects to `/` |
| `GET /quotes/<id>/` | Displays one quote, or returns 404 if it does not exist |
| `HEAD /quotes/<id>/` | Retrieves response headers without a response body |
| Other methods on `/quotes/<id>/` | Return 405 Method Not Allowed |
| `/admin/` | Django's administration interface |

```text
Browser request
    → config/urls.py
    → deliveries/urls.py
    → view function
    → template and context
    → HTML response
```

The detail view uses `get_object_or_404(Quote, pk=pk)` and `@require_safe` to allow
GET and HEAD. `pk` is the primary key identifying a quote.

Templates receive a context dictionary. `{{ quote.postcode }}` displays a value,
`{% for quote in quotes %}` loops over records, and `{% url 'quote_detail' quote.pk %}`
builds a link from a named URL. The extra `deliveries` directory under `templates`
keeps these template names distinct from other apps.

Using GET to retrieve and POST to create follows HTTP method semantics. Displaying
the form and history on the same page is a layout choice, not a REST requirement.
This application returns HTML rather than implementing a JSON API.

## Splitting views into files

`views.py` was replaced by a `views` package. `home.py` handles the form and list;
`quote_detail.py` retrieves a single quote. `views/__init__.py` exports the functions:

```python
from .home import home
from .quote_detail import quote_detail
```

The URL configuration can therefore keep using `views.home` and
`views.quote_detail`. Imports inside the package use `..models` or `..forms` to
reach the parent `deliveries` package. URL configuration belongs in `urls.py`;
request-handling functions belong in the views package.

## Forms and validation

### Tailwind styling

Both pages extend `templates/deliveries/base.html`, which loads Tailwind CSS v4
using its browser CDN. There is no npm build step. Start Django and refresh the
page to see the styled form, responsive history table, and quote detail card.

Utility classes in templates control spacing, colours, typography, and responsive
layout. `DeliveryQuoteForm.__init__()` adds the input classes to Django's widgets.
Validation errors and keyboard focus indicators have their own styling.

This follows [Tailwind's Play CDN setup](https://tailwindcss.com/docs/installation/play-cdn),
which is intended for development and requires internet access in the browser.
For deployment, replace the CDN with a compiled stylesheet served through Django
static files. The admin continues to use Django's built-in styling.

`DeliveryQuoteForm` defines a positive decimal weight, a required postcode, and a
choice of standard or express delivery. The postcode field checks presence and
length, not full UK postcode validity.

On GET, the view creates an empty form. On POST, it binds `request.POST` to the form:

```python
form = DeliveryQuoteForm(request.POST)
if form.is_valid():
    details = form.cleaned_data
```

Only after validation does the view use `cleaned_data`, which contains converted
values such as a `Decimal` weight. Invalid submissions render the form with errors.
`{{ form.as_p }}` renders fields and errors; `{% csrf_token %}` supplies Django's
protection against forged form submissions.

## Pricing, strategy, and dependency injection

`pricing.py` contains ordinary Python classes:

- `DeliveryCalculator` is a Protocol describing `calculate(weight) -> Decimal`.
- `StandardDelivery` and `ExpressDelivery` implement interchangeable pricing rules.
- `ShippingService` receives a calculator through its constructor and delegates to it.
- `calculator_for()` selects the implementation from the validated delivery type.

```python
service = ShippingService(calculator_for(details["delivery_type"]))
cost = service.quote(details["weight"])
```

The alternatives are the **strategy pattern**. Supplying the calculator is
**dependency injection**. The Protocol provides a typed interface without requiring
inheritance. `Decimal` keeps the calculation in decimal arithmetic, and the
template formats prices to two decimal places.

## Saving quotes and refreshing the page

`Quote` inherits from `models.Model`. Its fields describe database columns:
weight, postcode, delivery type, cost, and creation time. Django supplies a primary
key automatically. A Django model is different from a dataclass: it participates
in database queries and persistence.

The view uses `Quote.objects.create(...)` to insert a record and
`Quote.objects.all()` to retrieve history. Model ordering puts the newest records
first, with primary key as a tie-breaker.

After saving, the view stores the latest price as a string in the session and
redirects to the main page. The next request displays that price once. This is
the **POST/Redirect/GET** pattern: a normal refresh after the redirect does not
resubmit the form. It does not prevent duplicate records from separate repeated
submissions.

All saved quotes are currently visible to every visitor. There are no per-user
quote owners or filters in this learning version, and history is not paginated.

## Migrations

After changing database fields in `models.py`, generate a migration:

```sh
python manage.py makemigrations deliveries
```

This compares model definitions with migration state and writes a change file.
It does not yet modify the database. Apply pending migrations with:

```sh
python manage.py migrate
```

Check their status:

```sh
python manage.py showmigrations deliveries
```

`[X]` means applied; `[ ]` means pending. The initial migration creates the Quote
table. Commit migration files alongside model changes. Changes only to views or
templates do not require a database migration.

## Admin

Create an administrator account:

```sh
python manage.py createsuperuser
```

Visit <http://127.0.0.1:8000/admin/> and sign in. `admin.py` registers `Quote`, making
records available alongside Users and Groups. The quote list displays price,
weight, postcode, type, and creation time, with postcode search and a type filter.

Admin is a management interface for trusted staff. The public form and history
are separate views. Editing a quote in admin does not automatically recalculate
its cost using the pricing service.

## Checks and tests

From the `django` folder:

```sh
python manage.py check
python manage.py test deliveries
```

The tests cover valid prices and persistence, invalid submissions, empty and
ordered history, history after validation errors, detail pages, missing records,
and allowed detail methods. Django uses a separate test database.

### Why check for None before reading cost?

`Quote.objects.first()` can return `None` if no record exists. Tests therefore use:

```python
quote = Quote.objects.first()
assert quote is not None, "Submitting a valid form should save a quote."
self.assertEqual(quote.cost, Decimal(expected))
```

The assertion fails if saving did not happen and narrows the type for Pylance.
Checking `hasattr()` and calling `.first()` again neither narrows the second
result reliably nor ensures the price assertion runs when a record is missing.
