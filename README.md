## `POST /api/auth/users/`

### Description

This endpoint is used to create a new user account.

### Request Body

```json
{
  "username": "user",
  "email": "user@example.com",
  "password": "password123",
  "userType": "customer",
  "shopId": 1
  ...
}
```

### Response Body

```json
{
  "id": 1,
  "email": "user@example.com"
  ...
}
```

## `POST /api/token/`

### Description

This endpoint is used to obtain an access token and a refresh token for a user.

### Request Body

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Response Body

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## `POST /api/token/refresh/`

### Description

This endpoint is used to obtain a new access token using a refresh token.

### Request Body

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Response Body

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## `POST /api/token/verify/`

### Description

This endpoint is used to verify the validity of an access token.

### Request Body

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Response Body

```json
{
  "message": "Token is valid."
}
```

## `GET /api/users/`

### Description

This endpoint is used to retrieve a list of all users.

### Response Body

```json
[
  {
    "id": 1,
    "email": "user1@example.com",
    ...
  },
  {
    "id": 2,
    "email": "user2@example.com",
    ...
  }
]
```

## `GET /api/users/{id}/`

### Description

This endpoint is used to retrieve a specific user by ID.

### Response Body

```json
{
  "id": 1,
  "email": "user@example.com",
  ...
}
```

## `GET /api/products/`

### Description

This endpoint is used to retrieve a list of all products.

### Response Body

```json
[
  {
    "id": 1,
    "name": "Product 1",
    "description": "Description of Product 1",
    "price": 10.99,
    "shopId": 2
  },
  {
    "id": 2,
    "name": "Product 2",
    "description": "Description of Product 2",
    "price": 19.99,
    "shopId": 2
  }
]
```

## `POST /api/products/`

### Description

This endpoint is used to create a new product.

### Request Body

```json
{
  "name": "Product 1",
  "description": "Description of Product 1",
  "price": 10.99,
  "shopId": <int: shopId>
}
```

### Response Body

```json
{
  "id": 1,
  "name": "Product 1",
  "description": "Description of Product 1",
  "price": 10.99,
  "shopId": 2
}
```

## `GET /api/products/{id}/`

### Description

This endpoint is used to retrieve a specific product by ID.

### Response Body

```json
{
  "id": 1,
  "name": "Product 1",
  "description": "Description of Product 1",
  "price": 10.99,
  "shopId": 2
}
```

## `PUT /api/products/{id}/`

### Description

This endpoint is used to update a specific product by ID.

### Request Body

```json
{
  "name": "Updated Product 1",
  "description": "Updated description of Product 1",
  "price": 12.99
}
```

### Response Body

```json
{
  "id": 1,
  "name": "Updated Product 1",
  "description": "Updated description of Product 1",
  "price": 12.99,
  "shopId": 2
}
```

## `DELETE /api/products/{id}/`

### Description

This endpoint is used to delete a specific product by ID.

### Response Body

```json
{
  "message": "Product deleted successfully."
}
```

## `GET /api/shops/`

### Description

This endpoint is used to retrieve a list of all shops.

### Response Body

```json
[
  {
    "id": 1,
    "name": "Shop 1",
    "description": "Description of Shop 1",
    "shopOwner": 1
  },
  {
    "id": 2,
    "name": "Shop 2",
    "description": "Description of Shop 2",
    "shopOwner": 2
  }
]
```

## `POST /api/shops/`

### Description

This endpoint is used to create a new shop.

### Request Body

```json
{
  "name": "Shop 1",
  "description": "Description of Shop 1",
  "shopOwner": 1
}
```

### Response Body

```json
{
  "id": 1,
  "name": "Shop 1",
  "description": "Description of Shop 1",
  "shopOwner": 1
}
```

## `GET /api/shops/{id}/`

### Description

This endpoint is used to retrieve a specific shop by ID.

### Response Body

```json
{
  "id": 1,
  "name": "Shop 1",
  "description": "Description of Shop 1",
  "shopOwner": 1
}
```

## `PUT /api/shops/{id}/`

### Description

This endpoint is used to update a specific shop by ID.

### Request Body

```json
{
  "name": "Updated Shop 1",
  "description": "Updated description of Shop 1"
}
```

### Response Body

```json
{
  "id": 1,
  "name": "Updated Shop 1",
  "description": "Updated description of Shop 1"
}
```

## `DELETE /api/shops/{id}/`

### Description

This endpoint is used to delete a specific shop by ID.

### Response Body

```json
{
  "message": "Shop deleted successfully."
}
```

## `GET /api/carts/`

### Description

This endpoint is used to retrieve a list of all carts.

### Response Body

```json
[
  {
    "id": 1,
    "userId": 1,
    "products": [
      {
        "productId": 1,
        "name": "Product 1",
        "description": "Description of Product 1",
        "price": 10.99,
        "quantity": 2
      },
      {
        "productId": 2,
        "name": "Product 2",
        "description": "Description of Product 2",
        "price": 19.99,
        "quantity": 1
      }
    ]
  },
  {
    "id": 2,
    "userId": 2,
    "products": [
      {
        "productId": 1,
        "name": "Product 1",
        "description": "Description of Product 1",
        "price": 10.99,
        "quantity": 1
      }
    ]
  }
]
```

## `GET /api/carts/{id}/`

### Description

This endpoint is used to retrieve a specific cart by ID.

### Response Body

```json
{
  "id": 1,
  "userId": 1,
  "products": [
    {
      "productId": 1,
      "name": "Product 1",
      "description": "Description of Product 1",
      "price": 10.99,
      "quantity": 2
    },
    {
      "productId": 2,
      "name": "Product 2",
      "description": "Description of Product 2",
      "price": 19.99,
      "quantity": 1
    }
  ]
}
```

## `GET /api/user/cart/`

### Description

This endpoint is used to retrieve the cart of the currently authenticated user.

### Response Body

```json
{
  "id": 1,
  "userId": 1,
  "products": [
    {
      "productId": 1,
      "name": "Product 1",
      "description": "Description of Product 1",
      "price": 10.99,
      "quantity": 2
    },
    {
      "productId": 2,
      "name": "Product 2",
      "description": "Description of Product 2",
      "price": 19.99,
      "quantity": 1
    }
  ]
}
```

## `POST /api/cart/add/`

### Description

This endpoint is used to add a product to the cart of the currently authenticated user.

### Request Body

```json
{
  "productId": 1,
  "quantity": 1
}
```

### Response Body

```json
{
  "success": "Product added to cart successfully."
}
```

## `POST /api/cart/remove/`

### Description

This endpoint is used to remove a product from the cart of the currently authenticated user.

### Request Body

```json
{
  "productId": 1
}
```

### Response Body

```json
{
  "success": "Product removed from cart successfully."
}
```

## `POST /api/cart/update/`

### Description

This endpoint is used to update the quantity of a product in the cart of the currently authenticated user.

### Request Body

```json
{
  "productId": 1,
  "quantity": 3
}
```

### Response Body

```json
{
  "success": "Product quantity updated successfully."
}
```
