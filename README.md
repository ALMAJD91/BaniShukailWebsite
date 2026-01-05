# Bani Shukail Website (Django Backend)

This project converts your HTML/CSS frontend into a Django (server-side templates) web application.


## Clone Repository

open terminal and run the following commands:
```bash
cd Desktop
git clone https://github.com/abdulmalik123456/BaniShukailWebsite.git
cd BaniShukailWebsite
```

## Quick start (Local)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- http://127.0.0.1:8000/login/
- http://127.0.0.1:8000/admin/

## Render deployment (2 months then cancel)

**Web Service**
- Build command:
  `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Start command:
  `gunicorn bani_shukail.wsgi:application`

**Env vars on Render**
- `SECRET_KEY` (generate a strong key)
- `DEBUG=0`
- `ALLOWED_HOSTS=<your-app>.onrender.com`
- `CSRF_TRUSTED_ORIGINS=https://<your-app>.onrender.com`
- `DATABASE_URL=<Postgres URL from Neon (recommended) or Render Postgres>`
- `DB_SSL_REQUIRE=1` (usually required for managed Postgres)

## Notes
- Static files are served via WhiteNoise.
- Invoices/LPO create pages currently save up to 2 items (same as your frontend table).
