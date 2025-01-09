# E-commerce Backend API Documentation

## Base URL
The base URL for the API is:
```
http://127.0.0.1:5000
```

---

## Authentication Endpoints

### 1. Register User
**Endpoint:** `/register`

**Method:** `POST`

**Request Payload:**
```json
{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "password": "securepassword"
}
```

**Response:**
- **201 Created**:
```json
{
  "message": "User registered successfully"
}
```
- **400 Bad Request**:
```json
{
  "error": "Email already exists"
}
```

---

### 2. Login User
**Endpoint:** `/login`

**Method:** `POST`

**Request Payload:**
```json
{
  "email": "johndoe@example.com",
  "password": "securepassword"
}
```

**Response:**
- **200 OK**:
```json
{
  "message": "Login successful",
  "token": "<JWT-Token>"
}
```
- **401 Unauthorized**:
```json
{
  "error": "Invalid credentials"
}
```

---

## Product Endpoints

### 3. Get All Products
**Endpoint:** `/products`

**Method:** `GET`

**Response:**
- **200 OK**:
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "price": 1000,
    "category": "Electronics"
  },
  {
    "id": 2,
    "name": "Phone",
    "price": 500,
    "category": "Electronics"
  }
]
```

---

### 4. Add a Product
**Endpoint:** `/products`

**Method:** `POST`

**Request Payload:**
```json
{
  "name": "Tablet",
  "price": 300,
  "category": "Electronics"
}
```

**Response:**
- **201 Created**:
```json
{
  "message": "Product added successfully",
  "product": {
    "id": 3,
    "name": "Tablet",
    "price": 300,
    "category": "Electronics"
  }
}
```
- **400 Bad Request**:
```json
{
  "error": "Invalid product data"
}
```

---

## Wishlist Endpoints

### 5. Get Wishlist
**Endpoint:** `/wishlist`

**Method:** `GET`

**Response:**
- **200 OK**:
```json
[
  {
    "product_id": 1,
    "product_name": "Laptop",
    "price": 1000
  }
]
```
- **404 Not Found**:
```json
{
  "error": "Wishlist is empty"
}
```

---

### 6. Add to Wishlist
**Endpoint:** `/wishlist`

**Method:** `POST`

**Request Payload:**
```json
{
  "product_id": 1
}
```

**Response:**
- **200 OK**:
```json
{
  "message": "Product added to wishlist"
}
```

---

### 7. Remove from Wishlist
**Endpoint:** `/wishlist/<product_id>`

**Method:** `DELETE`

**Response:**
- **200 OK**:
```json
{
  "message": "Product removed from wishlist"
}
```
- **404 Not Found**:
```json
{
  "error": "Product not found in wishlist"
}
```

---

## Order Endpoints

### 8. Create Order
**Endpoint:** `/orders`

**Method:** `POST`

**Request Payload:**
```json
{
  "products": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 2, "quantity": 1}
  ]
}
```

**Response:**
- **201 Created**:
```json
{
  "message": "Order placed successfully",
  "order": {
    "id": 101,
    "date": "2025-01-09",
    "total": 2500
  }
}
```
- **400 Bad Request**:
```json
{
  "error": "Invalid order data"
}
```

---

### 9. Get Order History
**Endpoint:** `/orders`

**Method:** `GET`

**Response:**
- **200 OK**:
```json
[
  {
    "id": 101,
    "date": "2025-01-09",
    "total": 2500,
    "products": [
      {"product_id": 1, "quantity": 2, "price": 1000},
      {"product_id": 2, "quantity": 1, "price": 500}
    ]
  }
]
```

---

## Review Endpoints

### 10. Add Review
**Endpoint:** `/reviews`

**Method:** `POST`

**Request Payload:**
```json
{
  "product_id": 1,
  "rating": 5,
  "comment": "Excellent product!"
}
```

**Response:**
- **201 Created**:
```json
{
  "message": "Review added successfully"
}
```

---

### 11. Get Reviews for a Product
**Endpoint:** `/reviews/<product_id>`

**Method:** `GET`

**Response:**
- **200 OK**:
```json
[
  {
    "rating": 5,
    "comment": "Excellent product!",
    "user": "John Doe"
  }
]
```
- **404 Not Found**:
```json
{
  "error": "No reviews found for this product"
}
```