import requests
import json

# Base URL
base_url = "http://localhost:8000"

# Create a new test user to avoid conflicts
test_user = {
    "email": "testuser@example.com",
    "password": "testpassword123"
}

print("Testing the full flow...")

# 1. Register a new user
print("\n1. Registering new user...")
try:
    register_response = requests.post(f"{base_url}/api/auth/register", json=test_user)
    print(f"Register status: {register_response.status_code}")
    if register_response.status_code != 200:
        print(f"Register response: {register_response.text}")
except Exception as e:
    print(f"Register error: {e}")

# 2. Login to get a fresh token
print("\n2. Logging in to get token...")
try:
    login_response = requests.post(f"{base_url}/api/auth/login", json=test_user)
    print(f"Login status: {login_response.status_code}")
    if login_response.status_code == 200:
        login_data = login_response.json()
        token = login_data.get("access_token")
        print(f"Got token: {token is not None}")
    else:
        print(f"Login response: {login_response.text}")
        token = None
except Exception as e:
    print(f"Login error: {e}")
    token = None

if token:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 3. Test creating a todo with priority
    print("\n3. Creating todo with priority...")
    try:
        todo_data = {
            "title": "Test Todo from Python Script",
            "description": "This is a test todo created via script",
            "priority": "high",
            "due_date": "2025-12-31"
        }

        create_response = requests.post(f"{base_url}/api/todos", json=todo_data, headers=headers)
        print(f"Create todo status: {create_response.status_code}")

        if create_response.status_code == 200:
            created_todo = create_response.json()
            print(f"Created todo with ID: {created_todo.get('id')}")
            print(f"Priority: {created_todo.get('priority')}")
            print(f"Title: {created_todo.get('title')}")
        else:
            print(f"Create response: {create_response.text}")
    except Exception as e:
        print(f"Create todo error: {e}")

    # 4. Get all todos to verify
    print("\n4. Getting all todos...")
    try:
        get_response = requests.get(f"{base_url}/api/todos", headers=headers)
        print(f"Get todos status: {get_response.status_code}")

        if get_response.status_code == 200:
            todos = get_response.json()
            print(f"Number of todos: {len(todos)}")
            for i, todo in enumerate(todos):
                print(f"  Todo {i+1}: {todo.get('title')} - Priority: {todo.get('priority')}")
        else:
            print(f"Get response: {get_response.text}")
    except Exception as e:
        print(f"Get todos error: {e}")
else:
    print("\nFailed to get authentication token!")

print("\nTest completed.")