# Django REST Framework — Smart Inventory & Order Management System

A production-ready Django REST Framework backend for the Smart Inventory & Order Management System. This project implements a comprehensive inventory management API with JWT authentication, role-based access control, and real-time order processing.

## 📋 Implementation Status

This project follows the Software Requirements Specification (SRS) document for the Smart Inventory & Order Management System.

| Module | Feature                                  | Status          |
| ------ | ---------------------------------------- | --------------- |
| **B1** | **Project Bootstrap & Authentication**   | ✅ **Complete** |
|        | ├─ Custom User Model (UUID, Role-based)  | ✅              |
|        | ├─ JWT Authentication                    | ✅              |
|        | ├─ User Registration                     | ✅              |
|        | ├─ Login & Token Refresh                 | ✅              |
|        | ├─ Current User Profile                  | ✅              |
|        | └─ Demo User Seeding                     | ✅              |
| **B2** | **Categories & Products**                | ✅ **Complete** |
|        | ├─ Category Model & CRUD                 | ✅              |
|        | ├─ Product Model with Auto-Status        | ✅              |
|        | ├─ Product Filtering & Search            | ✅              |
|        | ├─ Stock Status Management               | ✅              |
|        | ├─ Low Stock Detection                   | ✅              |
|        | └─ Soft Delete (Archiving)               | ✅              |
| **B3** | **Orders**                               | ✅ **Complete** |
|        | ├─ Order & OrderItem Models              | ✅              |
|        | ├─ Auto Order Number Generation          | ✅              |
|        | ├─ Multi-Item Order Creation             | ✅              |
|        | ├─ Automatic Stock Deduction             | ✅              |
|        | ├─ Stock Validation & Conflict Check     | ✅              |
|        | ├─ Status Lifecycle Management           | ✅              |
|        | └─ Order Cancellation with Stock Restore | ✅              |
| **B4** | **Restock Queue**                        | ✅ **Complete** |
|        | ├─ RestockQueue Model                    | ✅              |
|        | ├─ Auto Queue Management                 | ✅              |
|        | ├─ Priority Calculation (High/Med/Low)   | ✅              |
|        | ├─ Manual Restock Endpoint               | ✅              |
|        | └─ Queue Listing & Removal               | ✅              |
| **B5** | **Activity Log**                         | 🔄 Pending      |
| **B6** | **Dashboard Stats**                      | 🔄 Pending      |
| **B7** | **Deployment**                           | 🔄 Pending      |

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

### Module B2 — Categories & Products (Implemented ✅)

- ✅ **Category Management** - Full CRUD operations
- ✅ **Product Management** - Complete inventory control
- ✅ **Automatic Status Management** - Auto-update based on stock
- ✅ **Advanced Filtering** - Filter by status, category, search
- ✅ **Low Stock Detection** - Automatic threshold monitoring
- ✅ **Soft Delete** - Archive products while preserving history
- ✅ **Validation** - Comprehensive input validation

### Module B3 — Orders (Implemented ✅)

- ✅ **Order Creation** - Multi-item orders in atomic transactions
- ✅ **Automatic Order Numbers** - Format: ORD-{YYYYMMDD}-{####}
- ✅ **Stock Validation** - Check availability before order creation
- ✅ **Automatic Stock Deduction** - Reduce inventory on order placement
- ✅ **Status Lifecycle** - pending → confirmed → shipped → delivered
- ✅ **Order Cancellation** - Restore stock when order is cancelled
- ✅ **Advanced Filtering** - Filter by status, date, customer search

### Module B4 — Restock Queue (Implemented ✅)

- ✅ **Automatic Queue Management** - Products auto-added when low stock
- ✅ **Priority Calculation** - High/Medium/Low based on stock levels
- ✅ **Manual Restocking** - Add stock via API endpoint
- ✅ **Smart Re-evaluation** - Auto-remove when stock sufficient
- ✅ **Ordered Listing** - Lowest stock products first

### Coming Soon (SRS Modules B5-B7)

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

### HTTP Only Cookie Based Authentication
The complete specification is available in [HTTP_COOKIE_AUTHENTICATION](HTTP_COOKIE_AUTH.md).


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

## � Module B2 — Categories & Products (Implemented ✅)

This project implements a complete inventory management system with automatic status management and comprehensive filtering.

### Category Model

Categories organize products into logical groups:

| Field        | Type      | Description                               |
| ------------ | --------- | ----------------------------------------- |
| `id`         | UUID      | Primary key (UUID4)                       |
| `name`       | CharField | Unique category name (max 100 characters) |
| `created_by` | FK User   | User who created the category             |
| `created_at` | DateTime  | Timestamp when category was created       |

**Features:**

- ✅ Unique category names
- ✅ Automatic product count tracking
- ✅ Delete protection (prevents deletion if products exist)

### Product Model

Products represent inventory items with automatic status management:

| Field                 | Type         | Description                                |
| --------------------- | ------------ | ------------------------------------------ |
| `id`                  | UUID         | Primary key (UUID4)                        |
| `name`                | CharField    | Product name (max 200 characters)          |
| `category`            | FK Category  | Product category                           |
| `price`               | DecimalField | Product price (2 decimal places, min 0)    |
| `stock_quantity`      | IntegerField | Current stock level (min 0)                |
| `min_stock_threshold` | IntegerField | Minimum stock threshold for alerts (min 0) |
| `status`              | CharField    | Product status (auto-managed)              |
| `created_by`          | FK User      | User who created the product               |
| `created_at`          | DateTime     | Timestamp when product was created         |
| `updated_at`          | DateTime     | Timestamp when product was last updated    |

**Product Status (Auto-Managed):**

- `active` - Product is available with stock > 0
- `out_of_stock` - Stock quantity has reached 0
- `archived` - Product is soft-deleted (preserved for history)

**Automatic Status Management:**
The product model automatically manages status based on stock quantity:

```python
# When stock reaches 0
stock_quantity == 0  →  status = 'out_of_stock'

# When stock is replenished
stock_quantity > 0 AND status == 'out_of_stock'  →  status = 'active'
```

**Computed Properties:**

- `is_low_stock` - Returns `True` if `stock_quantity < min_stock_threshold`

### Category API Endpoints

All category endpoints are prefixed with `/api/categories/`:

| Method | Endpoint                | Auth Required | Description                               |
| ------ | ----------------------- | ------------- | ----------------------------------------- |
| GET    | `/api/categories/`      | Yes           | List all categories with product counts   |
| POST   | `/api/categories/`      | Yes           | Create a new category                     |
| GET    | `/api/categories/{id}/` | Yes           | Get category details                      |
| PATCH  | `/api/categories/{id}/` | Yes           | Update category name                      |
| DELETE | `/api/categories/{id}/` | Yes           | Delete category (fails if products exist) |

**Category List Response:**

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Electronics",
    "created_by": "550e8400-e29b-41d4-a716-446655440001",
    "created_by_email": "user@example.com",
    "product_count": 15,
    "created_at": "2025-06-10T10:00:00Z"
  }
]
```

**Create Category Request:**

```json
{
  "name": "Electronics"
}
```

### Product API Endpoints

All product endpoints are prefixed with `/api/products/`:

| Method | Endpoint              | Auth Required | Description                   |
| ------ | --------------------- | ------------- | ----------------------------- |
| GET    | `/api/products/`      | Yes           | List products with filtering  |
| POST   | `/api/products/`      | Yes           | Create a new product          |
| GET    | `/api/products/{id}/` | Yes           | Get product details           |
| PATCH  | `/api/products/{id}/` | Yes           | Update product fields         |
| DELETE | `/api/products/{id}/` | Yes           | Archive product (soft delete) |

**Product List Query Parameters:**

| Parameter  | Type   | Description            | Example            |
| ---------- | ------ | ---------------------- | ------------------ |
| `status`   | string | Filter by status       | `?status=active`   |
| `category` | UUID   | Filter by category ID  | `?category={uuid}` |
| `search`   | string | Search in product name | `?search=iPhone`   |
| `ordering` | string | Order results          | `?ordering=-price` |

**Status Filter Values:**

- `active` - Only active products
- `out_of_stock` - Only out of stock products
- `archived` - Only archived products

**Ordering Options:**

- `name` - Sort by name (A-Z)
- `-name` - Sort by name (Z-A)
- `price` - Sort by price (low to high)
- `-price` - Sort by price (high to low)
- `stock_quantity` - Sort by stock (low to high)
- `-stock_quantity` - Sort by stock (high to low)
- `created_at` - Sort by creation date (oldest first)
- `-created_at` - Sort by creation date (newest first)

**Product List Response:**

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "iPhone 13",
      "category": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Electronics"
      },
      "price": "999.00",
      "stock_quantity": 3,
      "min_stock_threshold": 5,
      "status": "active",
      "is_low_stock": true,
      "created_at": "2025-06-10T10:00:00Z"
    }
  ]
}
```

**Product Detail Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "iPhone 13",
  "category": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Electronics"
  },
  "price": "999.00",
  "stock_quantity": 3,
  "min_stock_threshold": 5,
  "status": "active",
  "is_low_stock": true,
  "created_by": "550e8400-e29b-41d4-a716-446655440002",
  "created_by_email": "user@example.com",
  "created_at": "2025-06-10T10:00:00Z",
  "updated_at": "2025-06-10T12:00:00Z"
}
```

**Create Product Request:**

```json
{
  "name": "iPhone 13",
  "category": "550e8400-e29b-41d4-a716-446655440001",
  "price": "999.00",
  "stock_quantity": 10,
  "min_stock_threshold": 5
}
```

**Update Product Request (Partial):**

```json
{
  "stock_quantity": 20,
  "price": "899.00"
}
```

**Note:** Status is automatically managed based on stock quantity. You cannot manually set the status field.

### Validation Rules (Module B2)

**Category Validation:**

- ✅ Name must be unique (case-sensitive)
- ✅ Name cannot be empty or exceed 100 characters
- ✅ Cannot delete category if products exist

**Product Validation:**

- ✅ All fields are required on creation
- ✅ Price must be non-negative (>= 0)
- ✅ Stock quantity must be non-negative (>= 0)
- ✅ Minimum stock threshold must be non-negative (>= 0)
- ✅ Category must exist and be valid
- ✅ Cannot update archived products (must restore first)
- ✅ Status is automatically managed (cannot be manually set)

**Error Response Examples:**

```json
// Invalid price
{
  "price": ["Price must be non-negative."]
}

// Category with products cannot be deleted
{
  "detail": "Cannot delete category 'Electronics' because it has 15 product(s). Remove or reassign the products first."
}

// Cannot update archived product
{
  "detail": "Cannot update archived products. Restore the product first."
}
```

### Quick Test - Categories & Products (Module B2)

Test the Category and Product endpoints using curl:

**1. Create a Category:**

```bash
curl -X POST http://localhost:8000/api/categories/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronics"
  }'
```

**2. List Categories:**

```bash
curl -X GET http://localhost:8000/api/categories/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

**3. Create a Product:**

```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 13",
    "category": "<CATEGORY_UUID>",
    "price": "999.00",
    "stock_quantity": 10,
    "min_stock_threshold": 5
  }'
```

**4. List Products with Filters:**

```bash
# List all active products
curl -X GET "http://localhost:8000/api/products/?status=active" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Search for products
curl -X GET "http://localhost:8000/api/products/?search=iPhone" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Filter by category and order by price
curl -X GET "http://localhost:8000/api/products/?category=<UUID>&ordering=-price" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

**5. Update Product Stock:**

```bash
curl -X PATCH http://localhost:8000/api/products/<PRODUCT_UUID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "stock_quantity": 0
  }'
# Status automatically changes to 'out_of_stock'
```

**6. Archive a Product:**

```bash
curl -X DELETE http://localhost:8000/api/products/<PRODUCT_UUID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
# Product is soft-deleted (status = archived)
```

**7. Try to Delete Category with Products:**

```bash
curl -X DELETE http://localhost:8000/api/categories/<CATEGORY_UUID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
# Returns 400 error if products exist
```

### Module B2 Implementation Details

**Git Commit:** `feat(products): category & product CRUD, status auto-management`

**Files Modified/Created:**

- `products/models.py` - Category and Product models with auto-status logic
- `products/serializers.py` - All category and product serializers
- `products/views.py` - CategoryViewSet and ProductViewSet with filtering
- `products/urls.py` - API routing for categories and products
- `products/admin.py` - Django admin configuration with visual indicators

**Key Features:**

1. **UUID Primary Keys** - All models use UUIDs for better security
2. **Automatic Status Management** - Products auto-update status based on stock
3. **Soft Delete** - Products are archived instead of deleted
4. **Comprehensive Filtering** - Advanced query parameters for product listing
5. **Validation** - Input validation at serializer and model levels
6. **Optimized Queries** - Select/prefetch related for performance
7. **Low Stock Detection** - Computed property for stock alerts
8. **Delete Protection** - Categories cannot be deleted if products exist

## 📦 Module B3 — Orders (Implemented ✅)

This module implements a complete order management system with multi-item support, automatic stock deduction, and comprehensive status lifecycle management.

### Order Model

Orders represent customer purchases with automatic order number generation and status tracking:

| Field           | Type         | Description                                    |
| --------------- | ------------ | ---------------------------------------------- |
| `id`            | UUID         | Primary key (UUID4)                            |
| `order_number`  | CharField    | Auto-generated: `ORD-{YYYYMMDD}-{4-digit-seq}` |
| `customer_name` | CharField    | Customer name (max 200 characters)             |
| `status`        | CharField    | Order status (lifecycle managed)               |
| `total_price`   | DecimalField | Total order price (computed from items)        |
| `created_by`    | FK User      | User who created the order                     |
| `created_at`    | DateTime     | Timestamp when order was created               |
| `updated_at`    | DateTime     | Timestamp when order was last updated          |

**Order Status Lifecycle:**

```
pending    → confirmed | cancelled
confirmed  → shipped   | cancelled
shipped    → delivered
delivered  → (terminal — no further changes)
cancelled  → (terminal — no further changes)
```

**Automatic Order Number Generation:**

Order numbers follow the format `ORD-{YYYYMMDD}-{####}` where:

- `YYYYMMDD` is the current date (e.g., 20250610)
- `####` is a zero-padded 4-digit daily sequence (resets each day)
- Example: `ORD-20250610-0023`

### OrderItem Model

Order items represent individual products within an order:

| Field        | Type         | Description                     |
| ------------ | ------------ | ------------------------------- |
| `id`         | UUID         | Primary key (UUID4)             |
| `order`      | FK Order     | The order this item belongs to  |
| `product`    | FK Product   | The product being ordered       |
| `quantity`   | Integer      | Quantity ordered (min 1)        |
| `unit_price` | DecimalField | Price snapshot at order time    |
| `subtotal`   | DecimalField | Computed: quantity × unit_price |

**Features:**

- ✅ Price snapshot — captures product price at time of order
- ✅ Unique constraint — prevents duplicate products in same order
- ✅ Automatic subtotal calculation
- ✅ Protected deletion — product cannot be deleted if in orders

### Order API Endpoints

All order endpoints are prefixed with `/api/orders/`:

| Method | Endpoint                   | Auth Required | Description                      |
| ------ | -------------------------- | ------------- | -------------------------------- |
| GET    | `/api/orders/`             | Yes           | List orders with filtering       |
| POST   | `/api/orders/`             | Yes           | Create order with items (atomic) |
| GET    | `/api/orders/{id}/`        | Yes           | Get order detail with all items  |
| PATCH  | `/api/orders/{id}/status/` | Yes           | Update order status              |
| POST   | `/api/orders/{id}/cancel/` | Yes           | Cancel order and restore stock   |

**Order List Query Parameters:**

| Parameter  | Type   | Description                     | Example                 |
| ---------- | ------ | ------------------------------- | ----------------------- |
| `status`   | string | Filter by status                | `?status=pending`       |
| `search`   | string | Search customer name or order # | `?search=John`          |
| `ordering` | string | Order results                   | `?ordering=-created_at` |

**Status Filter Values:**

- `pending` - Pending orders
- `confirmed` - Confirmed orders
- `shipped` - Shipped orders
- `delivered` - Delivered orders
- `cancelled` - Cancelled orders

### Order Creation (Atomic Transaction)

Create an order with multiple items in a single atomic transaction. If any validation fails, the entire order creation is rolled back.

**POST** `/api/orders/`

**Request Body:**

```json
{
  "customer_name": "John Doe",
  "items": [
    {
      "product_id": "550e8400-e29b-41d4-a716-446655440000",
      "quantity": 2
    },
    {
      "product_id": "550e8400-e29b-41d4-a716-446655440001",
      "quantity": 1
    }
  ]
}
```

**Success Response (201 Created):**

```json
{
  "id": "650e8400-e29b-41d4-a716-446655440000",
  "order_number": "ORD-20250610-0023",
  "customer_name": "John Doe",
  "status": "pending",
  "total_price": "2997.00",
  "created_at": "2025-06-10T10:00:00Z",
  "updated_at": "2025-06-10T10:00:00Z",
  "items": [
    {
      "id": "750e8400-e29b-41d4-a716-446655440000",
      "product": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "iPhone 13"
      },
      "quantity": 2,
      "unit_price": "999.00",
      "subtotal": "1998.00"
    },
    {
      "id": "750e8400-e29b-41d4-a716-446655440001",
      "product": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "MacBook Pro"
      },
      "quantity": 1,
      "unit_price": "999.00",
      "subtotal": "999.00"
    }
  ]
}
```

### Order Creation Logic

The order creation process includes comprehensive validation and automatic actions:

1. **Validate Items** - At least one item required
2. **Duplicate Check** - No duplicate products in the same order
3. **Product Validation** - All products must exist and be active
4. **Stock Validation** - Sufficient stock available for each item
5. **Generate Order Number** - Automatic unique order number
6. **Create Order** - Create order with pending status
7. **Create Items** - Create all order items
8. **Snapshot Prices** - Capture current product prices
9. **Deduct Stock** - Reduce product stock quantities
10. **Compute Total** - Calculate total order price
11. **Update Restock Queue** - Check and update restock queue if needed

**All operations happen in an atomic transaction** — if any step fails, everything is rolled back.

### Order List Response

**GET** `/api/orders/`

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/orders/?page=2",
  "previous": null,
  "results": [
    {
      "id": "650e8400-e29b-41d4-a716-446655440000",
      "order_number": "ORD-20250610-0023",
      "customer_name": "John Doe",
      "status": "pending",
      "total_price": "2997.00",
      "item_count": 2,
      "created_at": "2025-06-10T10:00:00Z"
    }
  ]
}
```

### Order Detail Response

**GET** `/api/orders/{id}/`

Returns full order details including all items with nested product information.

### Update Order Status

Update the order status following the lifecycle rules.

**PATCH** `/api/orders/{id}/status/`

**Request Body:**

```json
{
  "status": "confirmed"
}
```

**Success Response (200 OK):**

Returns full order detail with updated status.

**Validation:**

- Status transition must be valid according to lifecycle rules
- Terminal states (delivered, cancelled) cannot be changed

### Cancel Order and Restore Stock

Cancel an order and automatically restore stock for all items.

**POST** `/api/orders/{id}/cancel/`

**Success Response (200 OK):**

```json
{
  "message": "Order cancelled successfully. Stock restored for all items.",
  "order": {
    "id": "650e8400-e29b-41d4-a716-446655440000",
    "order_number": "ORD-20250610-0023",
    "customer_name": "John Doe",
    "status": "cancelled",
    "total_price": "2997.00",
    "created_at": "2025-06-10T10:00:00Z",
    "updated_at": "2025-06-10T10:05:00Z",
    "items": [...]
  }
}
```

**Cancellation Logic:**

1. Validate status transition (must be cancellable)
2. Restore stock quantity for each item
3. Trigger product status updates (e.g., out_of_stock → active)
4. Update restock queue if needed
5. Set order status to cancelled

### Validation Rules (Module B3)

**Order Creation Validation:**

- ✅ At least one item required
- ✅ No duplicate products in order
- ✅ All products must exist
- ✅ All products must have `status = active`
- ✅ Sufficient stock for each item
- ✅ Quantity must be at least 1

**Status Transition Validation:**

- ✅ Must follow valid lifecycle transitions
- ✅ Cannot modify terminal states (delivered, cancelled)
- ✅ Cannot cancel delivered orders

**Error Response Examples:**

```json
// Duplicate product in order
{
  "items": ["Product 'iPhone 13' is already added to this order."]
}

// Product unavailable
{
  "items": ["Product 'iPhone 13' is currently unavailable."]
}

// Insufficient stock
{
  "items": ["Only 3 item(s) available for 'iPhone 13'."]
}

// Invalid status transition
{
  "detail": "Cannot transition from 'delivered' to 'cancelled'. Invalid status transition."
}
```

### Quick Test - Orders (Module B3)

Test the Order endpoints using curl:

**1. Create an Order:**

```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "items": [
      {"product_id": "<PRODUCT_UUID>", "quantity": 2},
      {"product_id": "<PRODUCT_UUID_2>", "quantity": 1}
    ]
  }'
```

**2. List Orders:**

```bash
# List all orders
curl -X GET http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Filter by status
curl -X GET "http://localhost:8000/api/orders/?status=pending" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Search by customer name
curl -X GET "http://localhost:8000/api/orders/?search=John" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

**3. Get Order Detail:**

```bash
curl -X GET http://localhost:8000/api/orders/<ORDER_UUID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

**4. Update Order Status:**

```bash
curl -X PATCH http://localhost:8000/api/orders/<ORDER_UUID>/status/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"status": "confirmed"}'
```

**5. Cancel Order:**

```bash
curl -X POST http://localhost:8000/api/orders/<ORDER_UUID>/cancel/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
# Stock is automatically restored for all items
```

### Module B3 Implementation Details

**Git Commit:** `feat(orders): order CRUD, stock deduction, status lifecycle`

**Files Created:**

- `orders/models.py` - Order and OrderItem models with lifecycle management
- `orders/serializers.py` - Comprehensive serializers with validation
- `orders/views.py` - OrderViewSet with custom actions
- `orders/urls.py` - API routing for orders
- `orders/admin.py` - Django admin with inline items display

**Key Features:**

1. **Atomic Transactions** - All-or-nothing order creation
2. **Automatic Order Numbers** - Daily sequence with date prefix
3. **Stock Validation** - Prevent overselling with comprehensive checks
4. **Automatic Stock Deduction** - Real-time inventory updates
5. **Status Lifecycle** - Enforced transition rules
6. **Price Snapshots** - Historical pricing preservation
7. **Stock Restoration** - Automatic when order is cancelled
8. **Restock Queue Integration** - Auto-update queue after stock changes
9. **Duplicate Prevention** - Unique constraint on order-product pairs
10. **Optimized Queries** - Select/prefetch related for performance

## 📦 Module B4 — Restock Queue (Implemented ✅)

This module implements an intelligent restock queue system with automatic management and priority-based ordering for low-stock products.

### RestockQueue Model

The restock queue automatically tracks products that need restocking:

| Field            | Type         | Description                            |
| ---------------- | ------------ | -------------------------------------- |
| `id`             | UUID         | Primary key (UUID4)                    |
| `product`        | OneToOne FK  | Product in restock queue (unique)      |
| `stock_quantity` | IntegerField | Current stock (cached for performance) |
| `added_at`       | DateTime     | Timestamp when added to queue          |

**Computed Properties:**

- `priority` - Returns `High`, `Medium`, or `Low` based on stock levels

**Priority Calculation (Auto-Computed):**

```python
# High Priority: Product completely out of stock
stock_quantity == 0  →  priority = 'High'

# Medium Priority: Stock is critically low (less than half threshold)
stock_quantity <= min_stock_threshold / 2  →  priority = 'Medium'

# Low Priority: Stock below threshold but not critical
stock_quantity < min_stock_threshold  →  priority = 'Low'
```

### Automatic Queue Management

The queue is **fully automated** — products are added and removed automatically based on stock levels:

**Auto-Add to Queue:**

```python
# Triggered when saving a product
if product.stock_quantity < product.min_stock_threshold:
    # Product is automatically added to restock queue
    RestockQueue.objects.get_or_create(product=product)
```

**Auto-Remove from Queue:**

```python
# Triggered after restocking
if product.stock_quantity >= product.min_stock_threshold:
    # Product is automatically removed from queue
    RestockQueue.objects.filter(product=product).delete()
```

**Features:**

- ✅ No manual queue management needed
- ✅ Real-time updates when stock changes
- ✅ Automatic re-evaluation after restocking
- ✅ Prevents duplicate entries (OneToOne relationship)

### Restock Queue API Endpoints

All restock queue endpoints are prefixed with `/api/restock/`:

| Method | Endpoint                     | Auth Required | Description                          |
| ------ | ---------------------------- | ------------- | ------------------------------------ |
| GET    | `/api/restock/`              | Yes           | List all products in restock queue   |
| GET    | `/api/restock/{id}/`         | Yes           | Get specific queue entry details     |
| POST   | `/api/restock/{id}/restock/` | Yes           | Add stock to product (custom action) |
| DELETE | `/api/restock/{id}/`         | Yes           | Manually remove from queue           |

**Note:** The restock queue is auto-managed. You **cannot** manually create queue entries via POST to `/api/restock/`. Products are automatically added when stock falls below threshold.

### Restock Queue List Response

The queue is automatically **ordered by stock_quantity ascending** (lowest stock first = highest urgency):

**GET** `/api/restock/`

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "product": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "iPhone 13",
        "category": "Electronics",
        "price": "999.00",
        "stock_quantity": 0,
        "min_stock_threshold": 5,
        "status": "out_of_stock"
      },
      "stock_quantity": 0,
      "priority": "High",
      "added_at": "2025-06-10T10:00:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "product": {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "name": "MacBook Pro",
        "category": "Electronics",
        "price": "2499.00",
        "stock_quantity": 2,
        "min_stock_threshold": 10,
        "status": "active"
      },
      "stock_quantity": 2,
      "priority": "Medium",
      "added_at": "2025-06-10T11:00:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440004",
      "product": {
        "id": "550e8400-e29b-41d4-a716-446655440005",
        "name": "AirPods Pro",
        "category": "Accessories",
        "price": "249.00",
        "stock_quantity": 8,
        "min_stock_threshold": 15,
        "status": "active"
      },
      "stock_quantity": 8,
      "priority": "Low",
      "added_at": "2025-06-10T12:00:00Z"
    }
  ]
}
```

### Restock Action (Add Stock)

Add stock to a product in the restock queue. The product will be **automatically removed** from the queue if stock reaches the threshold.

**POST** `/api/restock/{id}/restock/`

**Request Body:**

```json
{
  "quantity_to_add": 10
}
```

**Success Response (200 OK):**

```json
{
  "message": "Stock updated successfully. Product removed from restock queue.",
  "product": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "iPhone 13",
    "category": "Electronics",
    "price": "999.00",
    "stock_quantity": 10,
    "min_stock_threshold": 5,
    "status": "active"
  }
}
```

**If Stock Still Below Threshold (200 OK):**

```json
{
  "message": "Stock updated successfully. Product still in restock queue.",
  "product": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "iPhone 13",
    "category": "Electronics",
    "price": "999.00",
    "stock_quantity": 3,
    "min_stock_threshold": 5,
    "status": "active"
  }
}
```

**Validation Errors:**

```json
// Missing quantity
{
  "quantity_to_add": ["This field is required."]
}

// Invalid quantity
{
  "quantity_to_add": ["Must be greater than 0."]
}
```

### Manual Queue Removal

You can manually remove a product from the restock queue (useful for discontinued items):

**DELETE** `/api/restock/{id}/`

```bash
curl -X DELETE http://localhost:8000/api/restock/<QUEUE_ID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

**Success Response (204 No Content):**

```
(No response body)
```

**Note:** The product will be **automatically re-added** to the queue if stock is still below threshold when updated.

### Validation Rules (Module B4)

**Restock Action Validation:**

- ✅ `quantity_to_add` must be provided
- ✅ `quantity_to_add` must be greater than 0
- ✅ Quantity is added to current stock (not replaced)
- ✅ Stock updates trigger automatic queue re-evaluation

**Queue Management:**

- ✅ Products automatically added when stock < threshold
- ✅ Products automatically removed when stock >= threshold
- ✅ Cannot manually create queue entries (auto-managed only)
- ✅ Cannot have duplicate queue entries (OneToOne relationship)
- ✅ Queue ordered by urgency (stock_quantity ASC)

### Quick Test - Restock Queue (Module B4)

Test the Restock Queue endpoints using curl:

**1. Create a Low-Stock Product (Auto-Adds to Queue):**

```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 13",
    "category": "<CATEGORY_UUID>",
    "price": "999.00",
    "stock_quantity": 2,
    "min_stock_threshold": 10
  }'
# Product automatically added to restock queue
```

**2. List Restock Queue (Ordered by Urgency):**

```bash
curl -X GET http://localhost:8000/api/restock/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
# Returns all products needing restock, lowest stock first
```

**3. Get Queue Entry Details:**

```bash
curl -X GET http://localhost:8000/api/restock/<QUEUE_ID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

**4. Restock a Product (Auto-Removes if Sufficient):**

```bash
curl -X POST http://localhost:8000/api/restock/<QUEUE_ID>/restock/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity_to_add": 15
  }'
# Adds 15 to stock_quantity, auto-removes from queue if stock >= threshold
```

**5. Manually Remove from Queue:**

```bash
curl -X DELETE http://localhost:8000/api/restock/<QUEUE_ID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
# Removes from queue (will re-add if stock still low)
```

**6. Test Priority Levels:**

```bash
# High Priority (stock = 0)
curl -X PATCH http://localhost:8000/api/products/<PRODUCT_UUID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"stock_quantity": 0}'

# Medium Priority (stock <= threshold/2)
curl -X PATCH http://localhost:8000/api/products/<PRODUCT_UUID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"stock_quantity": 2}'  # If threshold is 10

# Low Priority (stock < threshold)
curl -X PATCH http://localhost:8000/api/products/<PRODUCT_UUID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"stock_quantity": 8}'  # If threshold is 10
```

### Module B4 Implementation Details

**Git Commit:** `feat(products): restock queue with auto-management & priority`

**Files Modified/Created:**

- `products/models.py` - RestockQueue model with priority property and check_restock_queue() helper
- `products/serializers.py` - RestockQueue, RestockQueueProduct, and RestockAction serializers
- `products/views.py` - RestockQueueViewSet with list, retrieve, restock action, destroy
- `products/urls.py` - API routing for restock queue
- `products/admin.py` - RestockQueueAdmin with color-coded priority display
- `products/migrations/0003_restockqueue.py` - Database migration for RestockQueue table

**Key Features:**

1. **Automatic Queue Management** - Products auto-add/remove based on stock levels
2. **Priority Calculation** - Three-tier priority system (High/Medium/Low)
3. **Smart Re-evaluation** - Queue updates automatically after stock changes
4. **Ordered by Urgency** - Lowest stock products appear first
5. **Restock Action** - Custom endpoint to add stock and auto-remove from queue
6. **OneToOne Relationship** - Prevents duplicate queue entries
7. **Cached Stock** - Performance optimization with denormalized stock_quantity
8. **Admin Color Coding** - Visual priority indicators (🔴 High, 🟠 Medium, 🔵 Low)

## �🔧 Configuration

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
