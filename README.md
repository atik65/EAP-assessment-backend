# 🏪 Smart Inventory & Order Management System

**A production-ready Django REST Framework API deployed on [Render](https://render.com/) using [Neon PostgreSQL](https://neon.tech/) (Free Tier)**

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-5ebaba?style=flat&logo=render)](https://eap-assessment-backend.onrender.com)
[![Database: Neon](https://img.shields.io/badge/Database-Neon%20DB-00e599?style=flat&logo=postgresql)](https://neon.tech/)

---

## 📋 Overview

A comprehensive REST API backend built with Django REST Framework that provides complete inventory and order management capabilities. Features include real-time stock tracking, automatic restock queue management, order processing with atomic transactions, and dashboard analytics.

**Perfect for:** E-commerce platforms, warehouse management, retail systems, or any business requiring robust inventory control.

---

## ✨ Key Features

### 🔐 Authentication & Authorization
- **JWT-based authentication** with access & refresh tokens
- **HTTP-only cookie support** for enhanced security
- **Role-based access control** (Admin, Manager, Staff)
- Custom user model with UUID primary keys

### 📦 Product Management
- Categories with product organization
- **Automatic stock status** (Active/Out of Stock/Archived)
- Low stock detection and alerts
- Soft delete (archiving) for data retention
- Advanced filtering and search

### 🛒 Order Processing
- **Atomic transaction handling** for order creation
- Auto-generated order numbers (`ORD-YYYYMMDD-####`)
- Multi-item orders with quantity validation
- **Automatic stock deduction** on order placement
- Order lifecycle management (Pending → Confirmed → Shipped → Delivered)
- **Stock restoration** on order cancellation

### 🔄 Smart Restock Queue
- **Automatic queue management** based on stock thresholds
- Priority calculation (High/Medium/Low)
- Real-time stock monitoring
- Manual restock operations with audit trail
- Auto-removal when stock is sufficient

### 📊 Dashboard Analytics
- Real-time KPI metrics (orders, revenue, stock status)
- Today's order and revenue statistics
- Low stock alerts and inventory health
- Product status overview
- Optimized aggregation queries

### 🪵 Activity Logging
- Comprehensive audit trail for all operations
- User action tracking (Create/Update/Delete)
- Entity-specific logging (Products, Orders, Categories)
- Timestamp and user attribution

---

## 🛠️ Tech Stack

**Backend Framework:**
- Django 5.2
- Django REST Framework 3.14
- **PostgreSQL (Neon Serverless DB)** / SQLite

**Authentication:**
- djangorestframework-simplejwt 5.3
- HTTP-only cookie support

**Additional Tools:**
- django-cors-headers (CORS handling)
- drf-spectacular (OpenAPI documentation)
- django-filter (Advanced filtering)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip
- virtualenv (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/eap-assessment-backend.git
cd eap-assessment-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create demo user (optional)
python manage.py seed_demo

# Start development server
python manage.py runserver
```

### 🔑 Demo Credentials

```
Email: demo@demo.com
Password: demo1234
Role: Admin
```

---

## 🌐 Live Demo

**Production API is live!** Try it out without any local setup:

**Base URL:** `https://eap-assessment-backend.onrender.com`

### Quick Test

```bash
# Login to get access token
curl -X POST https://eap-assessment-backend.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@demo.com","password":"demo1234"}'

# Get dashboard stats (replace YOUR_TOKEN with access token from above)
curl -X GET https://eap-assessment-backend.onrender.com/api/dashboard/stats/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### API Documentation

- **Swagger UI:** [https://eap-assessment-backend.onrender.com/api/docs/](https://eap-assessment-backend.onrender.com/api/docs)

**Note:** Demo data is shared across all users. Please be respectful when testing.

---

## 📡 API Endpoints

### Authentication
```
POST   /api/auth/register/       - Register new user
POST   /api/auth/login/          - Login (JWT tokens)
POST   /api/auth/token/refresh/  - Refresh access token
GET    /api/auth/me/             - Current user profile
```

### Products & Categories
```
GET    /api/categories/          - List categories
POST   /api/categories/          - Create category
GET    /api/products/            - List products (with filters)
POST   /api/products/            - Create product
PATCH  /api/products/{id}/       - Update product
DELETE /api/products/{id}/       - Archive product
```

### Orders
```
GET    /api/orders/              - List orders
POST   /api/orders/              - Create order (atomic)
GET    /api/orders/{id}/         - Order details
PATCH  /api/orders/{id}/status/  - Update status
POST   /api/orders/{id}/cancel/  - Cancel & restore stock
```

### Restock Queue
```
GET    /api/restock/             - List low stock items
POST   /api/restock/{id}/restock/ - Add stock to product
DELETE /api/restock/{id}/        - Remove from queue
```

### Dashboard
```
GET    /api/dashboard/stats/     - KPI metrics & analytics
```

### Activity Log
```
GET    /api/activity/            - Recent activity log
```

---

## 📂 Project Structure

```
inventory-api/
├── accounts/           # Authentication & User Management
├── products/           # Products, Categories, Restock Queue
├── orders/             # Order Processing
├── activity/           # Activity Logging
├── root_app/           # Django Settings
├── test_*.py           # API Test Scripts
└── requirements.txt    # Dependencies
```

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Test specific module
python manage.py test accounts
python manage.py test products
python manage.py test orders

# Quick API tests
python test_auth_api.py
python test_dashboard_stats.py
```

---

## 📖 Documentation


- **[HTTP Cookie Auth Guide](HTTP_COOKIE_AUTH.md)** - Secure cookie-based authentication
- **[SRS Document](srs.md)** - Software Requirements Specification


---

## 🎯 Use Cases

- **E-commerce Platforms**: Complete backend for online stores
- **Warehouse Management**: Track inventory across multiple locations
- **Retail Systems**: POS integration with inventory sync
- **Supply Chain**: Monitor stock levels and reorder points
- **B2B Platforms**: Multi-tenant inventory management

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file (optional):

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
PRODUCTION_URL=https://eap-assessment-backend.onrender.com
```

### Database

**Development:** SQLite (default)  
**Production:** PostgreSQL (recommended)

---

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in settings
- [ ] Configure PostgreSQL database
- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up CORS for frontend domain
- [ ] Enable HTTPS and secure cookies
- [ ] Set up Gunicorn/uWSGI
- [ ] Configure static files serving
- [ ] Set up database backups

### Docker Support

```bash
# Coming soon
docker-compose up
```

---

## 🎨 Frontend Integration

### React Example

```javascript
// API Base URL
const API_URL = 'https://eap-assessment-backend.onrender.com';
// For local development: const API_URL = 'http://localhost:8000';

// Login and fetch dashboard stats
const login = async () => {
  const response = await fetch(`${API_URL}/api/auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: 'demo@demo.com', password: 'demo1234' })
  });
  const { access } = await response.json();
  
  // Fetch dashboard stats
  const stats = await fetch(`${API_URL}/api/dashboard/stats/`, {
    headers: { 'Authorization': `Bearer ${access}` }
  });
  return await stats.json();
};
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**ATIK**
- GitHub: [@atik65](https://github.com/atik65)
- Production API: [https://eap-assessment-backend.onrender.com](https://eap-assessment-backend.onrender.com)

---

## 🙏 Acknowledgments

- Built with [Django REST Framework](https://www.django-rest-framework.org/)
- Authentication via [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- API documentation with [drf-spectacular](https://drf-spectacular.readthedocs.io/)

---

## 📊 Project Stats

- **Total Endpoints:** 25+
- **Models:** 7 (User, Category, Product, Order, OrderItem, RestockQueue, ActivityLog)
- **Test Coverage:** Comprehensive API tests included
- **Documentation:** 2000+ lines of detailed guides

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

🌐 **Live API:** [https://eap-assessment-backend.onrender.com](https://eap-assessment-backend.onrender.com/api/docs)

[Report Bug](https://github.com/yourusername/eap-assessment-backend/issues) · [Request Feature](https://github.com/yourusername/eap-assessment-backend/issues) · [Documentation](README.md)

</div>