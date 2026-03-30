# SRS — Backend (Django REST Framework)

**PROJECT:** Smart Inventory & Order Management System  
**LAYER:** Backend — Django REST Framework  
**VERSION:** 1.0  
**LAST UPDATED:** 2025-06-10  

---

## Overview

This document defines the backend API specification for the Smart Inventory & Order Management System. The backend is a Django REST Framework (DRF) project that exposes a JSON API consumed by a React frontend.

**Apps:** `accounts`, `products`, `orders`, `restock`, `activity`  
**Auth:** JWT (via `djangorestframework-simplejwt`)  
**Database:** PostgreSQL (prod) / SQLite (dev)  
**All endpoints require `Authorization: Bearer <access_token>` unless noted otherwise.**

---

## Module B1 — Project Bootstrap & Authentication

**Goal:** Runnable Django project with JWT auth, CORS, and a demo user.

### Setup Tasks

1. Create Django project named `inventory_api`.
2. Register apps: `accounts`, `products`, `orders`, `restock`, `activity`.
3. Install packages:
   ```
   djangorestframework
   djangorestframework-simplejwt
   django-cors-headers
   dj-database-url
   whitenoise
   django-filter
   ```
4. `settings.py` configuration:
   ```python
   REST_FRAMEWORK = {
       "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],
       "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
       "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
       "PAGE_SIZE": 20,
   }
   ```
5. CORS: allow `http://localhost:5173` in dev; use `CORS_ALLOWED_ORIGINS` env var in prod.
6. Custom User model in `accounts` (extend `AbstractUser`; add `role` field with choices: `admin` / `manager`, default `manager`).
7. Use `AUTH_USER_MODEL = "accounts.User"` in settings.

### User Model

| Field      | Type        | Notes                                          |
|------------|-------------|------------------------------------------------|
| `id`       | UUID        | Primary key                                    |
| `email`    | EmailField  | Unique, used as USERNAME_FIELD                 |
| `username` | CharField   | Keep for compatibility                         |
| `role`     | CharField   | Choices: `admin`, `manager`; default `manager` |

### Endpoints

| Method | URL                        | Auth | Description                                   |
|--------|----------------------------|------|-----------------------------------------------|
| POST   | `/api/auth/register/`      | No   | Register → 201 + `{access, refresh, user{}}` |
| POST   | `/api/auth/login/`         | No   | Login → 200 + `{access, refresh, user{}}`    |
| POST   | `/api/auth/token/refresh/` | No   | Refresh token → new access token             |
| GET    | `/api/auth/me/`            | Yes  | Current user profile                          |

### Response Shapes

**Login / Register response:**
```json
{
  "access": "<jwt>",
  "refresh": "<jwt>",
  "user": { "id": "uuid", "email": "user@example.com", "role": "manager" }
}
```

**`/api/auth/me/` response:**
```json
{ "id": "uuid", "email": "user@example.com", "role": "manager" }
```

### Validation Rules

- Email must be unique → 400 `{"email": ["A user with this email already exists."]}`
- Password minimum 8 characters → 400 `{"password": ["..."]}`
- All error responses use `{"detail": "..."}` or field-keyed dict — **no HTML error pages**.
- Set `DEBUG = False` error handler for 404/500 to return JSON.

### Demo User Seed

Management command: `python manage.py seed_demo`  
Creates: `demo@demo.com` / `demo1234` with `role = manager`  
(Idempotent — safe to run multiple times.)

**Git commit:** `feat(auth): JWT auth, custom user model, register/login endpoints`

---

## Module B2 — Categories & Products

**Goal:** Full CRUD for categories and products with automatic status management.

### Models

**Category**

| Field        | Type      | Notes           |
|--------------|-----------|-----------------|
| `id`         | UUID      | Primary key     |
| `name`       | CharField | Unique, max 100 |
| `created_by` | FK User   | Set on create   |
| `created_at` | DateTime  | Auto            |

**Product**

| Field                 | Type         | Notes                                           |
|-----------------------|--------------|-------------------------------------------------|
| `id`                  | UUID         | Primary key                                     |
| `name`                | CharField    | Max 200                                         |
| `category`            | FK Category  |                                                 |
| `price`               | DecimalField | 2 decimal places, min 0                         |
| `stock_quantity`      | IntegerField | Min 0                                           |
| `min_stock_threshold` | IntegerField | Min 0                                           |
| `status`              | CharField    | Choices: `active`, `out_of_stock`; auto-managed |
| `created_by`          | FK User      | Set on create                                   |
| `created_at`          | DateTime     | Auto                                            |
| `updated_at`          | DateTime     | Auto                                            |

**Status auto-management (override `save()`):**
- `stock_quantity == 0` → `status = out_of_stock`
- `stock_quantity > 0` and `status == out_of_stock` → `status = active`

### Endpoints

**Categories**

| Method | URL                     | Description                               |
|--------|-------------------------|-------------------------------------------|
| GET    | `/api/categories/`      | List all categories                       |
| POST   | `/api/categories/`      | Create category                           |
| GET    | `/api/categories/{id}/` | Category detail                           |
| PATCH  | `/api/categories/{id}/` | Update name only                          |
| DELETE | `/api/categories/{id}/` | Delete — block with 400 if products exist |

**Products**

| Method | URL                   | Description                                            |
|--------|-----------------------|--------------------------------------------------------|
| GET    | `/api/products/`      | List with filters (see below)                          |
| POST   | `/api/products/`      | Create product                                         |
| GET    | `/api/products/{id}/` | Product detail                                         |
| PATCH  | `/api/products/{id}/` | Update product fields                                  |
| DELETE | `/api/products/{id}/` | Soft-delete: set `status = archived`, keep for history |

**Product list query params:**
- `?status=active|out_of_stock`
- `?category={uuid}`
- `?search=` (name `icontains`)
- `?ordering=name|-price|-stock_quantity`

**Pagination:** all list endpoints → `{count, next, previous, results}` (page size 20)

### Serializer Output (Product)

```json
{
  "id": "uuid",
  "name": "iPhone 13",
  "category": { "id": "uuid", "name": "Electronics" },
  "price": "999.00",
  "stock_quantity": 3,
  "min_stock_threshold": 5,
  "status": "active",
  "is_low_stock": true,
  "created_at": "2025-06-10T10:00:00Z"
}
```

`is_low_stock` — computed `SerializerMethodField`: `stock_quantity < min_stock_threshold`.

**Git commit:** `feat(products): category & product CRUD, status auto-management`

---

## Module B3 — Orders

**Goal:** Order creation with multi-item support, automatic stock deduction, and status lifecycle.

### Models

**Order**

| Field           | Type         | Notes                                                                |
|-----------------|--------------|----------------------------------------------------------------------|
| `id`            | UUID         | Primary key                                                          |
| `order_number`  | CharField    | Auto-generated: `ORD-{YYYYMMDD}-{4-digit-seq}`                       |
| `customer_name` | CharField    | Max 200                                                              |
| `status`        | CharField    | Choices: `pending`, `confirmed`, `shipped`, `delivered`, `cancelled` |
| `total_price`   | DecimalField | Computed on save                                                     |
| `created_by`    | FK User      |                                                                      |
| `created_at`    | DateTime     | Auto                                                                 |
| `updated_at`    | DateTime     | Auto                                                                 |

**OrderItem**

| Field        | Type              | Notes                                     |
|--------------|-------------------|-------------------------------------------|
| `id`         | UUID              | Primary key                               |
| `order`      | FK Order          | `related_name="items"`                    |
| `product`    | FK Product        |                                           |
| `quantity`   | PositiveIntegerField | Min 1                                  |
| `unit_price` | DecimalField      | Snapshot of `product.price` at order time |
| `subtotal`   | DecimalField      | Computed: `quantity x unit_price`         |

### Endpoints

| Method | URL                         | Description                          |
|--------|-----------------------------|--------------------------------------|
| GET    | `/api/orders/`              | List orders (filtered)               |
| POST   | `/api/orders/`              | Create order + items (atomic)        |
| GET    | `/api/orders/{id}/`         | Order detail with all items          |
| PATCH  | `/api/orders/{id}/status/`  | Update status only                   |
| POST   | `/api/orders/{id}/cancel/`  | Cancel + restore stock               |

**Order list query params:** `?status=`, `?date=YYYY-MM-DD`, `?search=` (customer_name icontains)

### Order Creation Logic (atomic `transaction.atomic`)

1. Validate no duplicate products in `items` → 400 `{"detail": "Product '{name}' is already added to this order."}`
2. Validate all products have `status = active` → 400 `{"detail": "Product '{name}' is currently unavailable."}`
3. For each item: check `product.stock_quantity >= requested_quantity` → 400 `{"detail": "Only {n} items available for '{name}'."}`
4. Deduct `stock_quantity` for each item (triggers `Product.save()` status check).
5. Snapshot `unit_price = product.price`.
6. Compute `total_price = sum(item.quantity x item.unit_price)`.
7. Generate `order_number`: `ORD-{YYYYMMDD}-{zero-padded 4-digit daily sequence}`.
8. Call restock queue check for each affected product (Module B4).
9. Write activity log entry (Module B5).

### Status Transition Rules

```
pending    → confirmed | cancelled
confirmed  → shipped   | cancelled
shipped    → delivered
delivered  → (terminal — no further changes allowed)
cancelled  → (terminal — no further changes allowed)
```

- Return 400 `{"detail": "Invalid status transition."}` for any illegal move.
- **Cancel logic:** restore `stock_quantity` for each item → re-evaluate product statuses → re-evaluate restock queue.

### Serializer Output

**Order list item:**
```json
{
  "id": "uuid",
  "order_number": "ORD-20250610-0023",
  "customer_name": "Alice",
  "status": "pending",
  "total_price": "1998.00",
  "item_count": 2,
  "created_at": "2025-06-10T10:00:00Z"
}
```

**Order detail** — adds `items[]` array:
```json
{
  "id": "uuid",
  "order_number": "ORD-20250610-0023",
  "customer_name": "Alice",
  "status": "pending",
  "total_price": "1998.00",
  "created_at": "2025-06-10T10:00:00Z",
  "items": [
    {
      "id": "uuid",
      "product": { "id": "uuid", "name": "iPhone 13" },
      "quantity": 2,
      "unit_price": "999.00",
      "subtotal": "1998.00"
    }
  ]
}
```

**Git commit:** `feat(orders): order CRUD, stock deduction, conflict validation, status lifecycle`

---

## Module B4 — Restock Queue

**Goal:** Automatically populate and manage a low-stock priority queue.

### Model

**RestockQueue**

| Field      | Type              | Notes                             |
|------------|-------------------|-----------------------------------|
| `id`       | UUID              | Primary key                       |
| `product`  | OneToOne Product  |                                   |
| `added_at` | DateTime          | Auto                              |
| `priority` | —                 | Computed property, **not stored** |

**Priority logic (computed `@property`):**

| Condition                                                  | Priority |
|------------------------------------------------------------|----------|
| `stock_quantity == 0`                                      | `High`   |
| `1 <= stock_quantity <= floor(min_stock_threshold / 2)`   | `Medium` |
| Below threshold but above half                             | `Low`    |

### Auto-Queue Management

Call `check_restock_queue(product)` after every stock change (orders + manual restock):
- If `product.stock_quantity < product.min_stock_threshold` and not in queue → **add**.
- If `product.stock_quantity >= product.min_stock_threshold` and in queue → **remove**.

### Endpoints

| Method | URL                             | Description                                |
|--------|---------------------------------|--------------------------------------------|
| GET    | `/api/restock/`                 | List queue ordered by `stock_quantity ASC` |
| POST   | `/api/restock/{id}/restock/`    | Add stock, trigger queue re-evaluation     |
| DELETE | `/api/restock/{id}/`            | Manually remove from queue                 |

**Restock request body:** `{"quantity_to_add": 50}` — adds to existing stock, does not replace.

### Serializer Output

```json
{
  "id": "uuid",
  "product": {
    "id": "uuid",
    "name": "iPhone 13",
    "stock_quantity": 3,
    "min_stock_threshold": 5
  },
  "priority": "High",
  "added_at": "2025-06-10T10:00:00Z"
}
```

**Git commit:** `feat(restock): restock queue auto-management, priority logic, manual restock`

---

## Module B5 — Activity Log

**Goal:** Immutable, append-only audit trail. Returns the latest 50 entries.

### Model

**ActivityLog**

| Field          | Type      | Notes                                          |
|----------------|-----------|------------------------------------------------|
| `id`           | UUID      | Primary key                                    |
| `action`       | CharField | Max 500, human-readable                        |
| `performed_by` | FK User   | Nullable (for system events)                   |
| `timestamp`    | DateTime  | Auto                                           |
| `entity_type`  | CharField | Choices: `order`, `product`, `restock`, `auth` |
| `entity_id`    | UUIDField | Nullable                                       |

### Log Entry Formats

| Trigger                  | Message                                                |
|--------------------------|--------------------------------------------------------|
| Order created            | `"Order #{order_number} created by {username}"`        |
| Order status changed     | `"Order #{order_number} marked as {status}"`           |
| Order cancelled          | `"Order #{order_number} cancelled by {username}"`      |
| Product created          | `"Product '{name}' created by {username}"`             |
| Product updated          | `"Product '{name}' updated by {username}"`             |
| Stock manually restocked | `"Stock updated for '{product_name}' (+{qty} units)"`  |
| Product added to queue   | `"Product '{name}' added to Restock Queue"`            |

### Logging Convention

Use a class method: `ActivityLog.log(action, user, entity_type, entity_id)`

**Trigger from:** Order created / status changed / cancelled, Product created / updated, Stock restocked, Product added to restock queue.

### Endpoint

| Method | URL              | Description                               |
|--------|------------------|-------------------------------------------|
| GET    | `/api/activity/` | Latest 50 logs, newest first, no pagination |

**Git commit:** `feat(activity): activity log model and endpoint`

---

## Module B6 — Dashboard Stats

**Goal:** Single aggregation endpoint for the dashboard KPI cards.

### Endpoint

| Method | URL                     | Description           |
|--------|-------------------------|-----------------------|
| GET    | `/api/dashboard/stats/` | Dashboard KPI summary |

### Response

```json
{
  "orders_today": 12,
  "pending_orders": 5,
  "completed_orders": 7,
  "revenue_today": "14980.00",
  "low_stock_count": 3,
  "product_summary": [
    { "id": "uuid", "name": "iPhone 13", "stock_quantity": 3, "status": "low_stock" },
    { "id": "uuid", "name": "T-Shirt",   "stock_quantity": 20, "status": "ok" }
  ]
}
```

**Field definitions:**

| Field              | Logic                                                               |
|--------------------|---------------------------------------------------------------------|
| `orders_today`     | Count of all orders where `created_at__date = today`               |
| `pending_orders`   | Count of orders with `status = pending`                             |
| `completed_orders` | Count of `delivered` orders where `created_at__date = today`        |
| `revenue_today`    | Sum of `total_price` for non-cancelled orders created today         |
| `low_stock_count`  | Count of products where `stock_quantity < min_stock_threshold`      |
| `product_summary`  | All products; derived `status`: `low_stock` / `out_of_stock` / `ok` |

**Git commit:** `feat(dashboard): stats aggregation endpoint`

---

## Module B7 — Deployment

**Goal:** Production-ready configuration for Railway or Render.

### Tasks

1. Configure `whitenoise` middleware for static files serving.
2. Provide pinned `requirements.txt` and `Procfile`:
   ```
   web: gunicorn inventory_api.wsgi --log-file -
   release: python manage.py migrate && python manage.py seed_demo
   ```
3. All secrets via environment variables — no hardcoded values:

| Variable               | Required | Description                      |
|------------------------|----------|----------------------------------|
| `SECRET_KEY`           | Yes      | Django secret key                |
| `DEBUG`                | Yes      | `False` in production            |
| `DATABASE_URL`         | Yes      | PostgreSQL connection string     |
| `ALLOWED_HOSTS`        | Yes      | Comma-separated hostnames        |
| `CORS_ALLOWED_ORIGINS` | Yes      | Comma-separated frontend origins |

4. `python manage.py seed_demo` must be idempotent and work post-deploy.
5. `README.md` must include: local setup steps, env vars table, and live API base URL.

**Git commit:** `chore(deploy): production settings, Procfile, README`

---

## API Reference Summary

| Module     | Base URL               | Methods                  |
|------------|------------------------|--------------------------|
| Auth       | `/api/auth/`           | POST, GET                |
| Categories | `/api/categories/`     | GET, POST, PATCH, DELETE |
| Products   | `/api/products/`       | GET, POST, PATCH, DELETE |
| Orders     | `/api/orders/`         | GET, POST, PATCH         |
| Restock    | `/api/restock/`        | GET, POST, DELETE        |
| Activity   | `/api/activity/`       | GET                      |
| Dashboard  | `/api/dashboard/`      | GET                      |

---

## Implementation Order (Recommended)

```
B1 → B2 → B3 → B4 → B5 → B6 → B7
```

Each module builds on the previous. Implement, test, and git-commit before moving to the next.
