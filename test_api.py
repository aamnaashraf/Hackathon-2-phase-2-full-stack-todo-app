import requests
import json

# Base URL
base_url = "http://localhost:8000"

# Test data
test_user = {
    "email": "test@example.com",
    "password": "testpassword"
}

# Register user
print("Registering user...")
register_response = requests.post(f"{base_url}/api/auth/register", json=test_user)
print(f"Register response: {register_response.status_code}")

# Login to get token
print("Logging in...")
login_response = requests.post(f"{base_url}/api/auth/login", json=test_user)
login_data = login_response.json()
token = login_data.get("access_token")
print(f"Login response: {login_response.status_code}")

if token:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Test creating a todo with priority
    print("Creating todo with priority...")
    todo_data = {
        "title": "Test Todo with Priority",
        "description": "This is a test todo with priority",
        "priority": "high",
        "due_date": "2025-12-31"
    }

    create_response = requests.post(f"{base_url}/api/todos", json=todo_data, headers=headers)
    print(f"Create todo response: {create_response.status_code}")

    if create_response.status_code == 200:
        created_todo = create_response.json()
        print(f"Created todo: {json.dumps(created_todo, indent=2)}")

        # Get all todos
        print("Getting all todos...")
        get_response = requests.get(f"{base_url}/api/todos", headers=headers)
        print(f"Get todos response: {get_response.status_code}")

        if get_response.status_code == 200:
            todos = get_response.json()
            print(f"All todos: {json.dumps(todos, indent=2)}")
        else:
            print(f"Get todos failed: {get_response.text}")
    else:
        print(f"Create todo failed: {create_response.text}")
else:
    print("Failed to get token")