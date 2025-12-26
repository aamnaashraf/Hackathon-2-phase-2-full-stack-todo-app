# Data Model: Full-Stack Secure Todo Web Application

**Feature**: 1-secure-todo-app
**Date**: 2025-12-21

## Entity: User

**Description**: Represents a registered user of the todo application

**Fields**:
- `id` (UUID): Unique identifier for the user (primary key)
- `email` (String): User's email address (unique, required)
- `password_hash` (String): Hashed password for authentication (required)
- `created_at` (DateTime): Timestamp when user account was created (auto-generated)
- `updated_at` (DateTime): Timestamp when user account was last updated (auto-generated)
- `is_active` (Boolean): Whether the user account is active (default: true)

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum security requirements (at least 8 characters)
- Email and password are required for registration

**Relationships**:
- One-to-Many: User has many Todos (user_id foreign key in Todo table)

## Entity: Todo

**Description**: Represents a todo item owned by a specific user

**Fields**:
- `id` (UUID): Unique identifier for the todo (primary key)
- `title` (String): Title of the todo item (required, max 200 characters)
- `description` (String): Optional detailed description of the todo (max 1000 characters)
- `completed` (Boolean): Whether the todo is completed (default: false)
- `user_id` (UUID): Foreign key linking to the owning user (required)
- `created_at` (DateTime): Timestamp when todo was created (auto-generated)
- `updated_at` (DateTime): Timestamp when todo was last updated (auto-generated)
- `due_date` (DateTime, optional): Optional due date for the todo

**Validation Rules**:
- Title is required and must be between 1-200 characters
- Description is optional and must be less than 1000 characters if provided
- User_id must reference an existing user
- Completed status is boolean with default of false

**State Transitions**:
- New Todo: `completed = false` (default state when created)
- Completed Todo: `completed = true` (when user marks as complete)
- Reopened Todo: `completed = false` (when user reopens completed task)

**Relationships**:
- Many-to-One: Todo belongs to one User (via user_id foreign key)

## Database Schema Constraints

**User Table**:
- Primary Key: id
- Unique Constraint: email
- Index: email (for fast lookups during authentication)

**Todo Table**:
- Primary Key: id
- Foreign Key: user_id references User(id) with cascade delete
- Index: user_id (for fast filtering by user)
- Index: (user_id, completed) (for efficient queries of user's completed/incomplete todos)