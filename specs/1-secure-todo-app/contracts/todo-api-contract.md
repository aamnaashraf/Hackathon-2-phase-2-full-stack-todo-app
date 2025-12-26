# API Contracts: Full-Stack Secure Todo Web Application

## Authentication API

### POST /api/auth/register
**Description**: Register a new user account

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (201 Created)**:
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2025-12-21T10:30:00Z"
}
```

**Response (400 Bad Request)**:
```json
{
  "error": "Validation error message"
}
```

**Response (409 Conflict)**:
```json
{
  "error": "User with this email already exists"
}
```

### POST /api/auth/login
**Description**: Authenticate user and return JWT token

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK)**:
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  }
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Invalid credentials"
}
```

### POST /api/auth/logout
**Description**: Logout user (invalidate session)

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK)**:
```json
{
  "message": "Successfully logged out"
}
```

## Todo API

### GET /api/todos
**Description**: Get all todos for the authenticated user

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK)**:
```json
{
  "todos": [
    {
      "id": "uuid-string",
      "title": "Todo title",
      "description": "Optional description",
      "completed": false,
      "user_id": "user-uuid",
      "created_at": "2025-12-21T10:30:00Z",
      "updated_at": "2025-12-21T10:30:00Z",
      "due_date": "2025-12-31T23:59:59Z"
    }
  ]
}
```

### POST /api/todos
**Description**: Create a new todo for the authenticated user

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "title": "New todo title",
  "description": "Optional description",
  "due_date": "2025-12-31T23:59:59Z"
}
```

**Response (201 Created)**:
```json
{
  "id": "uuid-string",
  "title": "New todo title",
  "description": "Optional description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2025-12-21T10:30:00Z",
  "updated_at": "2025-12-21T10:30:00Z",
  "due_date": "2025-12-31T23:59:59Z"
}
```

### GET /api/todos/{id}
**Description**: Get a specific todo by ID

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK)**:
```json
{
  "id": "uuid-string",
  "title": "Todo title",
  "description": "Optional description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2025-12-21T10:30:00Z",
  "updated_at": "2025-12-21T10:30:00Z",
  "due_date": "2025-12-31T23:59:59Z"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "Todo not found"
}
```

### PUT /api/todos/{id}
**Description**: Update a specific todo by ID

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "due_date": "2025-12-31T23:59:59Z"
}
```

**Response (200 OK)**:
```json
{
  "id": "uuid-string",
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2025-12-21T10:30:00Z",
  "updated_at": "2025-12-21T11:00:00Z",
  "due_date": "2025-12-31T23:59:59Z"
}
```

### DELETE /api/todos/{id}
**Description**: Delete a specific todo by ID

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK)**:
```json
{
  "message": "Todo deleted successfully"
}
```