# Django REST Framework Boilerplate

A clean and ready-to-use Django REST Framework boilerplate with modern tooling and best practices. This boilerplate includes three example apps demonstrating different API patterns: main API, public API, and admin API.

## 🚀 Features

- **Django 5.2** - Latest Django framework
- **Django REST Framework** - Powerful REST API toolkit
- **Django Unfold** - Modern admin interface
- **DRF Spectacular** - OpenAPI 3.0 schema generation and Swagger UI
- **JWT Authentication** - Simple JWT token authentication
- **CORS Headers** - Cross-Origin Resource Sharing support
- **Django Filter** - Advanced filtering for REST API
- **SQLite Database** - Default database (easily switchable to PostgreSQL/MySQL)
- **Logging** - Comprehensive logging configuration
- **Three Example Apps** - Demonstrating different API patterns

## 📁 Project Structure

```
backend/
├── products/              # Main API app with full CRUD examples
│   ├── models.py         # Example model with timestamps
│   ├── serializers.py    # Example serializers (list, detail, create)
│   ├── views.py          # ViewSets and function-based views
│   ├── urls.py           # API routing with JWT auth
│   └── admin.py          # Django Unfold admin configuration
├── web_api/              # Public API app (no authentication)
│   ├── models.py         # Public-facing models
│   ├── serializers.py    # Public serializers
│   ├── views.py          # Public endpoints
│   └── urls.py           # Public routing
├── admin_api/            # Admin-only API app (requires auth)
│   ├── models.py         # Admin-specific models
│   ├── serializers.py    # Admin serializers
│   ├── views.py          # Admin-only endpoints
│   └── urls.py           # Admin routing
├── root_app/             # Django project settings
│   ├── settings.py       # Main configuration
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py/asgi.py   # WSGI/ASGI applications
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## 🎯 Three-App Architecture

### 1. **products/** - Main API

- Full CRUD operations with ViewSets
- Example model with relationships
- JWT authentication support
- Filtering, searching, and ordering
- Custom actions and endpoints

### 2. **web_api/** - Public API

- No authentication required
- Public-facing data
- Read-only endpoints typically
- Perfect for public content, blogs, etc.

### 3. **admin_api/** - Admin API

- Authentication required
- Admin-level permissions
- Sensitive operations
- Dashboard and statistics

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.11+
- pip
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

The server will start at http://localhost:8000/

## ?? API Documentation

Once the server is running, access the API documentation at:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔐 Authentication

### JWT Token Authentication

1. **Obtain Token**

   ```bash
   POST /api/token/
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

2. **Refresh Token**

   ```bash
   POST /api/token/refresh/
   {
     "refresh": "your_refresh_token"
   }
   ```

3. **Use Token**
   Add to request headers:
   ```
   Authorization: Bearer <your_access_token>
   ```

## 🔧 Configuration

### Django Settings

Key settings in [root_app/settings.py](root_app/settings.py):

- **CORS**: Configured for cross-origin requests
- **JWT**: Token-based authentication
- **DRF Spectacular**: API documentation
- **Django Unfold**: Modern admin interface
- **Logging**: Comprehensive logging setup

### Environment Variables (Optional)

Create a `.env` file for sensitive settings:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## 📊 API Endpoints

### Main API (products/)

**Example Model CRUD:**

- `GET /api/examples/` - List all example items
- `POST /api/examples/` - Create new item (auth required)
- `GET /api/examples/{id}/` - Get specific item
- `PUT /api/examples/{id}/` - Update item (auth required)
- `PATCH /api/examples/{id}/` - Partial update (auth required)
- `DELETE /api/examples/{id}/` - Delete item (auth required)

**Custom Actions:**

- `GET /api/examples/active/` - Get active items only
- `POST /api/examples/{id}/toggle_status/` - Toggle item status

**Utility Endpoints:**

- `GET /api/health/` - Health check endpoint
- `GET /api/statistics/` - Get statistics (auth required)

### Web API (web_api/) - Public Access

- `GET /web/info/` - Public API information (no auth required)

_Add your public endpoints here - perfect for blogs, public content, etc._

### Admin API (admin_api/) - Authenticated Access

- `GET /admin-api/info/` - Admin API information (auth required)
- `GET /admin-api/dashboard/` - Dashboard statistics (admin only)

_Add your admin-only endpoints here - dashboards, reports, user management, etc._

### Authentication Endpoints

- `POST /api/token/` - Obtain JWT access and refresh tokens
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token validity

## ?? Admin Panel

Access the Django Unfold admin panel at: http://localhost:8000/admin/

Features:

- Modern, responsive UI
- Dark mode support
- Advanced filtering and searching
- Inline editing
- Custom actions

## ?? Testing

Run tests with:

```bash
python manage.py test
```

## ?? Customization Guide

### 1. Create Your Own Models

Replace the example model in `products/models.py`:

```python
from django.db import models

class YourModel(models.Model):
    # Your fields here
    name = models.CharField(max_length=200)
    # ...
```

### 2. Create Serializers

Update `products/serializers.py`:

```python
from rest_framework import serializers
from .models import YourModel

class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModel
        fields = '__all__'
```

### 3. Create ViewSets

Update `products/views.py`:

```python
from rest_framework import viewsets
from .models import YourModel
from .serializers import YourModelSerializer

class YourModelViewSet(viewsets.ModelViewSet):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
```

### 4. Register URLs

Update `products/urls.py`:

```python
router.register(r'your-endpoint', views.YourModelViewSet)
```

### 5. Register in Admin

Update `products/admin.py`:

```python
@admin.register(YourModel)
class YourModelAdmin(ModelAdmin):
    list_display = ('name', ...)
```

## ??? Database Migration

### Switch to PostgreSQL

1. Install psycopg2:

   ```bash
   pip install psycopg2-binary
   ```

2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

## ?? Deployment

### Gunicorn (Production)

1. Install Gunicorn:

   ```bash
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn root_app.wsgi:application --bind 0.0.0.0:8000
   ```

### Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000
CMD ["gunicorn", "root_app.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## ?? License

This project is open source and available for use as a boilerplate/starter template.

## ?? Contributing

Feel free to modify and adapt this boilerplate for your own projects!

## ?? Support

For issues and questions, please open an issue in the repository.
# EAP-assessment-backend
