# Quick Start Guide — Module B6: Dashboard Stats

**Get dashboard KPI statistics in 3 minutes** 🚀

---

## 📋 What You'll Get

A single endpoint that returns:
- **Order Metrics**: Today's orders, pending orders, completed orders
- **Revenue**: Today's revenue (excluding cancelled orders)
- **Inventory Alerts**: Low stock product count
- **Product Status**: Complete product list with stock status

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start the Server

```bash
python manage.py runserver
```

### Step 2: Get Your Access Token

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@demo.com",
    "password": "demo1234"
  }'
```

**Save the `access` token from the response!**

### Step 3: Fetch Dashboard Stats

```bash
curl -X GET http://localhost:8000/api/dashboard/stats/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Done!** You now have all dashboard statistics.

---

## 📊 Example Response

```json
{
  "orders_today": 5,
  "pending_orders": 3,
  "completed_orders": 2,
  "revenue_today": "4999.95",
  "low_stock_count": 4,
  "product_summary": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "Laptop Pro 15",
      "stock_quantity": 2,
      "status": "low_stock"
    },
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "name": "Wireless Mouse",
      "stock_quantity": 0,
      "status": "out_of_stock"
    },
    {
      "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
      "name": "USB-C Cable",
      "stock_quantity": 50,
      "status": "ok"
    }
  ]
}
```

---

## 🎯 Understanding the Response

### Order Metrics

| Field              | What It Means                              | Example Use Case              |
|--------------------|--------------------------------------------|-------------------------------|
| `orders_today`     | All orders created today                   | "5 orders today"              |
| `pending_orders`   | Orders waiting to be confirmed             | "3 orders need attention"     |
| `completed_orders` | Orders delivered today                     | "2 orders completed today"    |
| `revenue_today`    | Money earned today (excluding cancellations) | "$4,999.95 earned today"   |

### Inventory Metrics

| Field            | What It Means                        | Example Use Case              |
|------------------|--------------------------------------|-------------------------------|
| `low_stock_count`| Products needing restock             | "⚠️ 4 items need restocking"  |

### Product Summary

Each product shows:
- `id`: Unique identifier
- `name`: Product name
- `stock_quantity`: Current stock level
- `status`: Visual indicator
  - ✅ `ok` - Stock is sufficient
  - ⚠️ `low_stock` - Stock below threshold
  - ❌ `out_of_stock` - No stock available

---

## 💻 Frontend Integration Examples

### React/Next.js

```javascript
// app/dashboard/page.js
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      const token = localStorage.getItem('access_token');
      
      const response = await fetch('http://localhost:8000/api/dashboard/stats/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      const data = await response.json();
      setStats(data);
      setLoading(false);
    };

    fetchStats();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      <div className="kpi-cards">
        <div className="card">
          <h3>Orders Today</h3>
          <p className="metric">{stats.orders_today}</p>
        </div>
        
        <div className="card">
          <h3>Revenue Today</h3>
          <p className="metric">${stats.revenue_today}</p>
        </div>
        
        <div className="card alert">
          <h3>Low Stock Items</h3>
          <p className="metric">{stats.low_stock_count}</p>
        </div>
      </div>

      <div className="product-list">
        <h2>Inventory Status</h2>
        {stats.product_summary.map(product => (
          <div key={product.id} className={`product ${product.status}`}>
            <span>{product.name}</span>
            <span>Stock: {product.stock_quantity}</span>
            <span className="badge">{product.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Vue.js

```vue
<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    
    <div v-if="loading">Loading...</div>
    
    <div v-else>
      <!-- KPI Cards -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <h3>Orders Today</h3>
          <div class="value">{{ stats.orders_today }}</div>
        </div>
        
        <div class="kpi-card">
          <h3>Revenue Today</h3>
          <div class="value">${{ stats.revenue_today }}</div>
        </div>
        
        <div class="kpi-card warning">
          <h3>Low Stock</h3>
          <div class="value">{{ stats.low_stock_count }}</div>
        </div>
      </div>

      <!-- Product List -->
      <div class="products">
        <h2>Inventory Status</h2>
        <div 
          v-for="product in stats.product_summary" 
          :key="product.id"
          :class="['product', product.status]"
        >
          <span>{{ product.name }}</span>
          <span>{{ product.stock_quantity }}</span>
          <span class="badge">{{ product.status }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      stats: null,
      loading: true
    }
  },
  async mounted() {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://localhost:8000/api/dashboard/stats/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    this.stats = await response.json();
    this.loading = false;
  }
}
</script>
```

### Vanilla JavaScript

```javascript
async function loadDashboard() {
  const token = localStorage.getItem('access_token');
  
  try {
    const response = await fetch('http://localhost:8000/api/dashboard/stats/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    const stats = await response.json();
    
    // Update KPI cards
    document.getElementById('orders-today').textContent = stats.orders_today;
    document.getElementById('revenue-today').textContent = `$${stats.revenue_today}`;
    document.getElementById('low-stock').textContent = stats.low_stock_count;
    
    // Render product list
    const productList = document.getElementById('product-list');
    stats.product_summary.forEach(product => {
      const div = document.createElement('div');
      div.className = `product ${product.status}`;
      div.innerHTML = `
        <span>${product.name}</span>
        <span>Stock: ${product.stock_quantity}</span>
        <span class="badge">${product.status}</span>
      `;
      productList.appendChild(div);
    });
    
  } catch (error) {
    console.error('Failed to load dashboard:', error);
  }
}

// Load on page ready
document.addEventListener('DOMContentLoaded', loadDashboard);
```

---

## 🧪 Test It Yourself

### Option 1: Use the Test Script

```bash
python test_dashboard_stats.py
```

### Option 2: Use Postman/Insomnia

1. **Create a request:**
   - Method: GET
   - URL: `http://localhost:8000/api/dashboard/stats/`
   
2. **Add Authorization Header:**
   - Key: `Authorization`
   - Value: `Bearer YOUR_ACCESS_TOKEN`
   
3. **Send the request!**

### Option 3: Use Browser (with Auth)

Install a browser extension like "ModHeader" to add the Authorization header, then visit:
```
http://localhost:8000/api/dashboard/stats/
```

---

## 🎨 Dashboard UI Ideas

### KPI Cards Layout

```
┌─────────────────┬─────────────────┬─────────────────┐
│  Orders Today   │  Revenue Today  │  Low Stock      │
│      12         │    $14,980      │      3          │
└─────────────────┴─────────────────┴─────────────────┘

┌─────────────────┬─────────────────┬─────────────────┐
│  Pending        │  Completed      │  Total Products │
│      5          │      7          │      45         │
└─────────────────┴─────────────────┴─────────────────┘
```

### Product Status Colors

- 🟢 **OK** (`ok`): Green - Stock is healthy
- 🟡 **Low Stock** (`low_stock`): Yellow/Orange - Warning
- 🔴 **Out of Stock** (`out_of_stock`): Red - Critical

---

## 🔍 Filtering Products by Status

```javascript
// Get only low stock products
const lowStockProducts = stats.product_summary.filter(
  p => p.status === 'low_stock'
);

// Get out of stock products
const outOfStock = stats.product_summary.filter(
  p => p.status === 'out_of_stock'
);

// Get products that need attention
const needsAttention = stats.product_summary.filter(
  p => p.status !== 'ok'
);
```

---

## ⚡ Auto-Refresh Dashboard

```javascript
// Refresh every 30 seconds
setInterval(async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://localhost:8000/api/dashboard/stats/', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const stats = await response.json();
  updateDashboard(stats);
}, 30000); // 30 seconds
```

---

## ❌ Troubleshooting

### Error: 401 Unauthorized

**Problem:** Missing or invalid token

**Solution:**
```bash
# Login again to get fresh token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@demo.com","password":"demo1234"}'
```

### Error: 404 Not Found

**Problem:** Wrong URL

**Solution:** Make sure you're using the correct endpoint:
```
✅ http://localhost:8000/api/dashboard/stats/
❌ http://localhost:8000/dashboard/stats/
❌ http://localhost:8000/api/stats/
```

### Empty Product Summary

**Problem:** No products in database

**Solution:** Create some products first:
```bash
# See Module B2 documentation for creating products
```

### All Zeros in Metrics

**Problem:** No data yet

**Solution:** This is normal for a fresh installation. Create:
- Products (Module B2)
- Orders (Module B3)
- Wait for today's data to accumulate

---

## 📈 Performance Tips

### 1. Cache the Response

```javascript
// Cache for 60 seconds
let cachedStats = null;
let cacheTime = 0;

async function getDashboardStats() {
  const now = Date.now();
  if (cachedStats && (now - cacheTime) < 60000) {
    return cachedStats;
  }
  
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://localhost:8000/api/dashboard/stats/', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  cachedStats = await response.json();
  cacheTime = now;
  return cachedStats;
}
```

### 2. Load Only What You Need

If you only need KPIs (not product summary):
```javascript
// Use the full data but only display what you need
const stats = await getDashboardStats();
// Only use: stats.orders_today, stats.revenue_today, etc.
// Ignore: stats.product_summary (if not displaying it)
```

---

## 🎓 Next Steps

1. ✅ Integrate into your frontend dashboard
2. ✅ Add visual charts (Chart.js, Recharts, etc.)
3. ✅ Set up auto-refresh
4. ✅ Add alerts for low stock items
5. ✅ Create mobile-responsive design

---

## 📚 Related Documentation

- [README.md](README.md) - Full project documentation
- [MODULE_B6_SUMMARY.md](MODULE_B6_SUMMARY.md) - Detailed implementation
- [srs.md](srs.md) - Software Requirements Specification

---

## ✅ Checklist

- [ ] Server is running (`python manage.py runserver`)
- [ ] Demo user exists (`python manage.py seed_demo`)
- [ ] Got access token (login endpoint)
- [ ] Tested dashboard stats endpoint
- [ ] Integrated into frontend
- [ ] Dashboard looks amazing! 🎉

---

**Happy Coding!** 🚀

For questions or issues, check the main README.md or MODULE_B6_SUMMARY.md