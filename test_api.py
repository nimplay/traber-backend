import requests

try:
    response = requests.get("http://localhost:8000/providers")
    print(f"Status: {response.status_code}")
    providers = response.json()
    print(f"Total providers returned: {len(providers)}")
    if len(providers) > 0:
        print(f"First provider: {providers[0]['name']}")
except Exception as e:
    print(f"Error: {e}")
