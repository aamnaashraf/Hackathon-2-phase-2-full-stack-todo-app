import requests
import json

# Base URL
base_url = "http://localhost:8000"

# Login to get token
login_response = requests.post(f"{base_url}/api/auth/login", json={
    "email": "test@example.com",
    "password": "testpassword"
})
login_data = login_response.json()
token = login_data.get("access_token")

if token:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Get all todos to find one to update
    get_response = requests.get(f"{base_url}/api/todos", headers=headers)
    todos = get_response.json()

    if todos:
        todo_id = todos[0]['id']
        print(f"Updating todo with ID: {todo_id}")

        # Update the todo with a new priority
        update_data = {
            "title": "Updated Todo with Medium Priority",
            "priority": "medium"
        }

        update_response = requests.put(f"{base_url}/api/todos/{todo_id}", json=update_data, headers=headers)
        print(f"Update response: {update_response.status_code}")

        if update_response.status_code == 200:
            updated_todo = update_response.json()
            print(f"Updated todo: {json.dumps(updated_todo, indent=2)}")
        else:
            print(f"Update failed: {update_response.text}")
    else:
        print("No todos found to update")
else:
    print("Failed to get token")