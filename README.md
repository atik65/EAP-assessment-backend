# Django REST Framework — Smart Inventory & Order Management System

A production-ready Django REST Framework backend for the Smart Inventory & Order Management System. This project implements a comprehensive inventory management API with JWT authentication, role-based access control, and real-time order processing.

## 📋 Implementation Status

This project follows the Software Requirements Specification (SRS) document for the Smart Inventory & Order Management System.

| Module | Feature                                 | Status          |
| ------ | --------------------------------------- | --------------- |
| **B1** | **Project Bootstrap & Authentication**  | ✅ **Complete** |
|        | ├─ Custom User Model (UUID, Role-based) | ✅              |
|        | ├─ JWT Authentication                   | ✅              |
|        | ├─ User Registration                    | ✅              |
|        | ├─ Login & Token Refresh                | ✅              |
|        | ├─ Current User Profile                 | ✅              |
|        | └─ Demo User Seeding                    | ✅              |
| **B2** | **Categories & Products**               | 🔄 Pending      |
| **B3** | **Orders**                              | 🔄 Pending      |
| **B4** | **Restock Queue**                       | 🔄 Pending      |
| **B5** | **Activity Log**                        | 🔄 Pending      |
| **B6** | **Dashboard Stats**                     | 🔄 Pending      |
| **B7** | **Deployment**                          | 🔄 Pending      |

## 🚀 Features

### Core Features (Implemented)

- ✅ **Django 5.2** - Latest Django framework
- ✅ **Django REST Framework** - Powerful REST API toolkit
- ✅ **JWT Authentication** - Simple JWT token authentication with refresh
- ✅ **Custom User Model** - UUID-based with role field (admin/manager)
- ✅ **Role-Based Access Control** - Admin and Manager roles
- ✅ **CORS Headers** - Cross-Origin Resource Sharing support
- ✅ **Django Filter** - Advanced filtering for REST API
- ✅ **DRF Spectacular** - OpenAPI 3.0 schema generation and Swagger UI
- ✅ **Django Unfold** - Modern admin interface
- ✅ **Demo User Seeding** - Quick setup for testing

### Database & Infrastructure

- **SQLite** - Default database (development)
- **PostgreSQL Ready** - Production database configuration
- **Pagination** - 20 items per page by default
- **Logging** - Comprehensive logging configuration
- **Atomic Transactions** - Database integrity for complex operations

### Coming Soon (SRS Modules B2-B7)

- 🔄 Categories & Products Management with auto-status
- 🔄 Order Processing with stock deduction
- 🔄 Restock Queue with priority management
- 🔄 Activity Logging (audit trail)
- 🔄 Dashboard Statistics & Analytics
- 🔄 Production Deployment Configuration

## 📁 Project Structure

```
backend/
├── accounts/             # Authentication & User Management (Module B1)
│   ├── models.py         # Custom User model with role field
│   ├── serializers.py    # Register, Login, User serializers
│   ├── views.py          # Register, Login, Current User views
│   ├── urls.py           # Auth endpoints routing
│   └── management/       # Management commands
│       └── commands/
│           └── seed_demo.py  # Demo user seeding
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

## 🎯 Application Architecture

### **accounts/** - Authentication & User Management (Module B1) ✅

- **Custom User Model** with UUIDs and role-based access
- **JWT Authentication** using djangorestframework-simplejwt
- **User Registration** with email validation
- **Login** with email/password authentication
- **Token Management** (access & refresh tokens)
- **Current User Profile** endpoint
- **Demo User Seeding** for quick testing
- **Role-Based Access Control** (Admin/Manager roles)

### **products/** - Main API

- Full CRUD operations with ViewSets
- Example model with relationships
- JWT authentication support
- Filtering, searching, and ordering
- Custom actions and endpoints

### **web_api/** - Public API

- No authentication required
- Public-facing data
- Read-only endpoints typically
- Perfect for public content, blogs, etc.

### **admin_api/** - Admin API

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

5. **Create demo user (optional)**

   ```bash
   python manage.py seed_demo
   ```

   This creates a test user: `demo@demo.com` / `demo1234`

6. **Create superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

The server will start at http://localhost:8000/

## ?? API Documentation

Once the server is running, access the API documentation at:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔐 Module B1 — Authentication & User Management (Implemented ✅)

This project implements a complete JWT-based authentication system with custom user model and role-based access control.

### Custom User Model

The system uses a custom User model that extends Django's `AbstractUser`:

| Field      | Type       | Description                                          |
| ---------- | ---------- | ---------------------------------------------------- |
| `id`       | UUID       | Primary key (UUID4)                                  |
| `email`    | EmailField | Unique, used as USERNAME_FIELD for authentication    |
| `username` | CharField  | Kept for compatibility                               |
| `role`     | CharField  | User role: `admin` or `manager` (default: `manager`) |

**Configuration:**

- `AUTH_USER_MODEL = 'accounts.User'` in settings.py
- Email is used as the primary authentication field
- All user IDs are UUIDs instead of integers for better security

### JWT Token Authentication

The system uses `djangorestframework-simplejwt` for JWT token authentication:

- **Access Token Lifetime:** 60 minutes
- **Refresh Token Lifetime:** 7 days
- **Token Rotation:** Enabled (new refresh token on each refresh)
- **Auth Header:** `Authorization: Bearer <access_token>`

### Authentication Endpoints

All authentication endpoints are prefixed with `/api/auth/`:

#### 1. Register User

**POST** `/api/auth/register/`

**Public endpoint** (no authentication required)

**Request Body:**

```json
{
  "email": "user@example.com",
  "username": "john_doe", // Optional, auto-generated from email if not provided
  "password": "securepass123",
  "password2": "securepass123", // Confirmation password
  "role": "manager" // Optional, defaults to "manager"
}
```

**Success Response (201 Created):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "john_doe",
    "role": "manager"
  }
}
```

**Error Responses:**

```json
// Email already exists (400 Bad Request)
{
  "email": ["A user with this email already exists."]
}

// Passwords don't match (400 Bad Request)
{
  "password": ["Password fields didn't match."]
}
```

#### 2. Login

**POST** `/api/auth/login/`

**Public endpoint** (no authentication required)

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Success Response (200 OK):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "john_doe",
    "role": "manager"
  }
}
```

**Error Response (401 Unauthorized):**

```json
{
  "detail": "Invalid email or password."
}
```

#### 3. Token Refresh

**POST** `/api/auth/token/refresh/`

**Public endpoint** (no authentication required)

Refresh an expired access token using a valid refresh token.

**Request Body:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response (200 OK):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..." // New refresh token (rotation enabled)
}
```

#### 4. Current User Profile

**GET** `/api/auth/me/`

**Authenticated endpoint** (requires valid access token)

Get the currently authenticated user's profile information.

**Request Headers:**

```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "john_doe",
  "role": "manager"
}
```

**Error Response (401 Unauthorized):**

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Using JWT Tokens

After successful login or registration, include the access token in the `Authorization` header for all authenticated requests:

```bash
# Example using curl
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
     http://localhost:8000/api/auth/me/
```

```javascript
// Example using fetch
fetch("http://localhost:8000/api/auth/me/", {
  headers: {
    Authorization: "Bearer eyJ0eXAiOiJKV1QiLCJhbGc...",
    "Content-Type": "application/json",
  },
});
```

### Demo User

For quick testing, a demo user is available:

**Email:** `demo@demo.com`  
**Password:** `demo1234`  
**Role:** `manager`

To create or reset the demo user, run:

```bash
python manage.py seed_demo
```

This command is **idempotent** — it's safe to run multiple times. If the user already exists, it will reset the password to `demo1234`.

### Validation Rules

- **Email:** Must be unique and valid email format
- **Password:** Minimum 8 characters (Django default validators)
- **Passwords Match:** `password` and `password2` must match during registration
- **Email Case-Insensitive:** Emails are stored as-is but searched case-insensitively

### CORS Configuration

The API is configured to accept requests from the following origins:

- `http://localhost:5173` (React/Vite dev server)
- `http://127.0.0.1:5173`

CORS credentials are enabled for cookie/token handling.

### REST Framework Configuration

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

**Important:** All API endpoints require authentication by default unless explicitly marked with `permission_classes = [AllowAny]`.

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
# Django Core
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (default: SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# CORS (for frontend integration)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# JWT Configuration (optional, defaults are set)
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=10080  # 7 days in minutes
```

**Module B1 Required Packages:**

```txt
Django>=5.2
djangorestframework>=3.14
djangorestframework-simplejwt>=5.3
django-cors-headers>=4.3
drf-spectacular>=0.27
```

## 📊 API Endpoints

### Authentication (accounts/) ✅ Module B1

**All endpoints prefixed with `/api/auth/`**

| Method | Endpoint                   | Auth Required | Description                                         |
| ------ | -------------------------- | ------------- | --------------------------------------------------- |
| POST   | `/api/auth/register/`      | No            | Register new user → 201 + `{access, refresh, user}` |
| POST   | `/api/auth/login/`         | No            | Login → 200 + `{access, refresh, user}`             |
| POST   | `/api/auth/token/refresh/` | No            | Refresh token → new access token                    |
| GET    | `/api/auth/me/`            | Yes           | Get current user profile                            |

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

## ?? Admin Panel

Access the Django Unfold admin panel at: http://localhost:8000/admin/

Features:

- Modern, responsive UI
- Dark mode support
- Advanced filtering and searching
- Inline editing
- Custom actions

## ?? Testing

### Quick Test - Authentication (Module B1)

Test the authentication endpoints using curl or any API client:

**1. Register a new user:**

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }'
```

**2. Login with demo user:**

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@demo.com",
    "password": "demo1234"
  }'
```

**3. Get current user profile:**

```bash
# Replace <ACCESS_TOKEN> with the token from login response
curl -X GET http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

**4. Refresh token:**

```bash
# Replace <REFRESH_TOKEN> with the refresh token from login
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<REFRESH_TOKEN>"}'
```

### Run Unit Tests

Run all tests with:

```bash
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test accounts
python manage.py test products
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

## 📖 Documentation

### Software Requirements Specification (SRS)

The complete project specification is available in [srs.md](srs.md). It contains detailed requirements for all modules (B1-B7).

### Module B1 — Authentication (Completed ✅)

**Git Commit:** `feat(auth): JWT auth, custom user model, register/login endpoints`

**Implementation Details:**

- **Custom User Model**: `accounts.User` with UUID primary key, email authentication, and role field
- **Serializers**: Register, Login, User, LoginResponse serializers
- **Views**: RegisterView, LoginView, current_user_view
- **Endpoints**: `/api/auth/register/`, `/api/auth/login/`, `/api/auth/token/refresh/`, `/api/auth/me/`
- **Demo User Seeding**: Management command `seed_demo` for creating test user
- **Validation**: Email uniqueness, password matching, minimum length enforcement
- **Error Handling**: JSON error responses for all validation failures

**Files Modified/Created:**

- `accounts/models.py` - Custom User model
- `accounts/serializers.py` - All auth serializers
- `accounts/views.py` - Registration and login views
- `accounts/urls.py` - Auth routing
- `accounts/management/commands/seed_demo.py` - Demo user command
- `root_app/settings.py` - JWT, REST Framework, CORS configuration

### API Testing Tools

- **Swagger UI**: http://localhost:8000/api/docs/ (interactive API documentation)
- **ReDoc**: http://localhost:8000/api/redoc/ (beautiful API docs)
- **Admin Panel**: http://localhost:8000/admin/ (Django Unfold interface)

## 📝 License

This project is open source and available for use as a boilerplate/starter template.

## ?? Contributing

Feel free to modify and adapt this boilerplate for your own projects!

## ?? Support

For issues and questions, please open an issue in the repository.

# EAP-assessment-backend
