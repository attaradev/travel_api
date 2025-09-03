# Travel API

A sample **Django REST API** for managing travel listings, bookings, and reviews.
Includes:

* **Django + DRF** for API endpoints
* **Swagger UI** at `/swagger/` for interactive documentation
* **Celery + RabbitMQ** for background jobs (e.g., sending booking emails)
* **Postgres** database
* **Mailhog** for local email testing
* **Render** blueprint for production deployment

---

## 🚀 Features

* Listings (CRUD)
* Bookings with validation (availability, overlap checks)
* Reviews with ratings
* Background email notifications (via Celery task)
* Public API documentation at `/swagger/`

---

## 🛠️ Local Development

### Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* `docker compose`

### Run services

```bash
docker compose up --build
```

Services started:

* **API** → [http://localhost:8000](http://localhost:8000)
* **Swagger** → [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
* **RabbitMQ Management UI** → [http://localhost:15672](http://localhost:15672) (guest/guest)
* **Mailhog UI** → [http://localhost:8025](http://localhost:8025)

### Run migrations

```bash
docker compose exec api python manage.py migrate
```

### Seed sample data

```bash
docker compose exec api python manage.py seed_listings
```

Now visit:

* `/api/listings/`
* `/api/bookings/`
* `/api/reviews/`

### Create superuser (optional)

```bash
docker compose exec api python manage.py createsuperuser
```

---

## 📦 Project Structure

```md
.
├── core/                   # Django project (settings, urls, wsgi, celery)
├── listings/               # App: models, serializers, views, management commands
│   ├── management/commands/seed_listings.py
├── docker-entrypoint.sh    # Entrypoint script (waits for DB & broker)
├── docker-compose.yml      # Local dev stack
├── Dockerfile              # Build instructions for app image
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment blueprint
└── README.md
```

---

## 📧 Emails in Dev

Emails are sent to **Mailhog**, accessible at:
👉 [http://localhost:8025](http://localhost:8025)

---

## ☁️ Deployment (Render)

This repo includes a **`render.yaml`** Blueprint. Steps:

1. Push your repo to GitHub.
2. In Render → **Blueprint Deploy**, pick your repo.
3. Provision services:

   * `travel-api-web` (Django web)
   * `travel-api-celery` (worker)
   * `travel-api-beat` (beat)
   * `travel-db` (Postgres)
4. Create a **CloudAMQP** instance (RabbitMQ) → paste its **`amqps://…`** URL into `CELERY_BROKER_URL` for all services.
5. Set environment variables (`EMAIL_*`, `PUBLIC_ORIGIN`, etc.).
6. Deploy!

Swagger docs:
👉 `https://<your-render-domain>/swagger/`

---

## 🔐 Environment Variables

| Key                     | Example / Notes                               |
| ----------------------- | --------------------------------------------- |
| `DJANGO_SECRET_KEY`     | Auto-generated in Render                      |
| `DEBUG`                 | `0` in prod, `1` in dev                       |
| `DATABASE_URL`          | Injected from Render Postgres                 |
| `CELERY_BROKER_URL`     | `amqps://...` from CloudAMQP                  |
| `CELERY_RESULT_BACKEND` | `rpc://` or Redis                             |
| `PUBLIC_ORIGIN`         | `https://your-app.onrender.com`               |
| `EMAIL_BACKEND`         | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST`            | e.g. `smtp.postmarkapp.com`                   |
| `EMAIL_PORT`            | usually `587`                                 |
| `EMAIL_HOST_USER`       | SMTP username                                 |
| `EMAIL_HOST_PASSWORD`   | SMTP password                                 |
| `EMAIL_USE_TLS`         | `1`                                           |
| `DEFAULT_FROM_EMAIL`    | `no-reply@yourdomain.com`                     |

---

## ✅ TODOs

* Add unit tests with `pytest`
* Improve CI/CD (GitHub Actions + Render deploy hooks)
* Add rate limiting / auth (JWT or session-based)
