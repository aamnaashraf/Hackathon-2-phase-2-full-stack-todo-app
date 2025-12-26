# Simple debugging script to test the token
import requests
import json

# Get the token from localStorage in the browser console
# In your browser console, run: localStorage.getItem('access_token')
# Then replace the token below with your actual token

# Example token from our test:
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzY2NjU2MzgxfQ.W5e_bfO8Z2cdY1Dhlh1lVGoAAU1WxwBm4qpprmwZ5P4"

# Get your actual token from localStorage in the browser:
# 1. Open your browser's developer tools
# 2. Go to the Console tab
# 3. Run: localStorage.getItem('access_token')
# 4. Copy the token and replace it below

your_token = input("Enter your token from localStorage: ").strip()

if your_token:
    headers = {
        "Authorization": f"Bearer {your_token}",
        "Content-Type": "application/json"
    }

    # Test getting todos with your token
    print("Testing your token...")
    response = requests.get("http://localhost:8000/api/todos", headers=headers)
    print(f"Response status: {response.status_code}")

    if response.status_code == 200:
        print("Token is valid! You can create todos.")
        todos = response.json()
        print(f"Number of todos: {len(todos)}")
    else:
        print(f"Token is invalid or expired. Response: {response.text}")
        print("Please log out and log back in to get a fresh token.")
else:
    print("No token provided. Please get your token from localStorage in the browser.")