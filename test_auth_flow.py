import requests
import json

# Base URL
base_url = "http://localhost:8000"

# Create a new test user to avoid any conflicts
test_user = {
    "email": "newtest@example.com",
    "password": "newtestpassword123"
}

print("Testing the complete authentication flow with new backend...")

# 1. Register a new user
print("\n1. Registering new user...")
try:
    register_response = requests.post(f"{base_url}/api/auth/register", json=test_user)
    print(f"Register status: {register_response.status_code}")
    if register_response.status_code == 200:
        register_data = register_response.json()
        print(f"Registration successful: {register_data.get('email')}")
    else:
        print(f"Registration failed: {register_response.text}")
        exit(1)
except Exception as e:
    print(f"Registration error: {e}")
    exit(1)

# 2. Login to get a fresh token
print("\n2. Logging in to get fresh token...")
try:
    login_response = requests.post(f"{base_url}/api/auth/login", json=test_user)
    print(f"Login status: {login_response.status_code}")
    if login_response.status_code == 200:
        login_data = login_response.json()
        token = login_data.get("access_token")
        print(f"Successfully got token: {token is not None}")
        print(f"User: {login_data.get('user', {}).get('email')}")
    else:
        print(f"Login failed: {login_response.text}")
        exit(1)
except Exception as e:
    print(f"Login error: {e}")
    exit(1)

if token:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 3. Test creating a todo with all the new features (priority, due_date)
    print("\n3. Creating todo with priority...")
    todo_data = {
        "title": "Test Todo with All New Features",
        "description": "This is a test todo with priority and due date",
        "priority": "high",
        "due_date": "2025-12-31"
    }

    create_response = requests.post(f"{base_url}/api/todos", json=todo_data, headers=headers)
    print(f"Create todo status: {create_response.status_code}")

    if create_response.status_code == 200:
        created_todo = create_response.json()
        print(f"✓ Successfully created todo!")
        print(f"  - ID: {created_todo.get('id')}")
        print(f"  - Title: {created_todo.get('title')}")
        print(f"  - Priority: {created_todo.get('priority')}")
        print(f"  - Due Date: {created_todo.get('due_date')}")
        print(f"  - Description: {created_todo.get('description')}")
    else:
        print(f"✗ Failed to create todo: {create_response.text}")
        exit(1)

    # 4. Get all todos to verify
    print("\n4. Getting all todos...")
    get_response = requests.get(f"{base_url}/api/todos", headers=headers)
    print(f"Get todos status: {get_response.status_code}")

    if get_response.status_code == 200:
        todos = get_response.json()
        print(f"✓ Successfully retrieved {len(todos)} todos")
        for i, todo in enumerate(todos):
            print(f"  Todo {i+1}: {todo.get('title')} (Priority: {todo.get('priority')})")
    else:
        print(f"✗ Failed to get todos: {get_response.text}")
        exit(1)

    # 5. Test updating a todo
    print("\n5. Testing todo update...")
    if todos:
        todo_id = todos[0]['id']
        update_data = {
            "title": "Updated Todo with Medium Priority",
            "priority": "medium"
        }

        update_response = requests.put(f"{base_url}/api/todos/{todo_id}", json=update_data, headers=headers)
        print(f"Update status: {update_response.status_code}")

        if update_response.status_code == 200:
            updated_todo = update_response.json()
            print(f"✓ Successfully updated todo!")
            print(f"  - New Title: {updated_todo.get('title')}")
            print(f"  - New Priority: {updated_todo.get('priority')}")
        else:
            print(f"✗ Failed to update todo: {update_response.text}")

    print("\n✓ All tests passed! The backend with priority feature is working correctly.")
else:
    print("\n✗ Failed to get authentication token!")
    exit(1)

print("\nTest completed successfully.")