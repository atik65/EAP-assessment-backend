# HTTP-Only Cookie Authentication

This implementation adds secure HTTP-only cookie-based authentication alongside the existing token-based auth.

## 🔐 Security Benefits

- **XSS Protection**: Tokens stored in HTTP-only cookies cannot be accessed by JavaScript
- **Automatic Token Management**: Browser handles cookie storage and sending
- **CSRF Protection**: SameSite cookie attribute prevents CSRF attacks

## 📡 New API Endpoints

### 1. HTTP-Only Login

**POST** `/api/auth/http-login/`

Login and receive JWT tokens in HTTP-only cookies.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "message": "Login successful"
}
```

**Cookies Set:**

- `access_token` (HTTP-only, 1 hour expiry)
- `refresh_token` (HTTP-only, 7 days expiry)

### 2. HTTP-Only Logout

**POST** `/api/auth/http-logout/`

Clear authentication cookies.

**Response:**

```json
{
  "message": "Logout successful"
}
```

## 💻 React Frontend Usage

### Setup Axios with Credentials

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  withCredentials: true, // IMPORTANT: Send cookies with requests
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
```

### Login Example

```javascript
import api from "./api";

const login = async (email, password) => {
  try {
    const response = await api.post("/auth/http-login/", {
      email,
      password,
    });

    console.log("Login successful:", response.data);
    // Cookies are automatically stored by the browser
    return response.data.user;
  } catch (error) {
    console.error("Login failed:", error.response?.data);
    throw error;
  }
};
```

### Logout Example

```javascript
const logout = async () => {
  try {
    await api.post("/auth/http-logout/");
    console.log("Logout successful");
    // Cookies are automatically cleared
  } catch (error) {
    console.error("Logout failed:", error);
  }
};
```

### Making Authenticated Requests

```javascript
// No need to manually add Authorization header!
// Cookies are sent automatically with withCredentials: true

const getCurrentUser = async () => {
  try {
    const response = await api.get("/auth/me/");
    return response.data;
  } catch (error) {
    console.error("Failed to get user:", error);
    throw error;
  }
};
```

### Complete React Hook Example

```javascript
import { useState, useEffect } from "react";
import api from "./api";

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await api.get("/auth/me/");
      setUser(response.data);
    } catch (error) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    const response = await api.post("/auth/http-login/", {
      email,
      password,
    });
    setUser(response.data.user);
    return response.data.user;
  };

  const logout = async () => {
    await api.post("/auth/http-logout/");
    setUser(null);
  };

  return { user, loading, login, logout };
};
```

## 🔄 Existing Features Still Work

The original authentication methods remain unchanged:

- **POST** `/api/auth/register/` - Register new user (returns tokens in response body)
- **POST** `/api/auth/login/` - Login (returns tokens in response body)
- **POST** `/api/auth/token/refresh/` - Refresh token
- **GET** `/api/auth/me/` - Get current user (works with both auth methods)

## 🔧 Production Deployment

For production, update [settings.py](root_app/settings.py) to enable secure cookies:

```python
# In HttpOnlyLoginView.post() method
response.set_cookie(
    key='access_token',
    value=tokens['access'],
    httponly=True,
    secure=True,      # Enable for HTTPS
    samesite='Strict', # Stricter CSRF protection
    max_age=3600,
)
```

Also update CORS settings to allow only your production domain:

```python
CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
]
```

## 📝 Notes

- Cookies work automatically when frontend and backend are on the same domain
- For cross-domain (e.g., localhost:3000 → localhost:8000), `withCredentials: true` is required
- `CookieJWTAuthentication` tries cookie first, then falls back to Authorization header
- Both authentication methods can coexist - use whichever fits your needs
