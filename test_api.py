import requests
import json

def get_user_input():
    print("--- Leakosint API Search Tool ---")
    token = input("Enter your API Token: ").strip()
    if not token:
        print("Token is required!")
        return None, None, None
    
    request_query = input("Enter your search request: ").strip()
    if not request_query:
        print("Search request is required!")
        return None, None, None

    limit_input = input("Enter search limit (default 100): ").strip()
    limit = 100
    if limit_input:
        try:
            limit = int(limit_input)
        except ValueError:
            print("Invalid limit. Using default 100.")
    
    return token, request_query, limit

def perform_search(token, request_query, limit):
    url = 'https://leakosintapi.com/'
    data = {
        "token": token,
        "request": request_query,
        "limit": limit,
        "lang": "en"
    }
    
    print(f"\nSending request to {url}...")
    try:
        response = requests.post(url, json=data)
        response.raise_for_status() # Raise error for bad status codes
        
        try:
            json_response = response.json()
            print("\n--- API Response ---")
            print(json.dumps(json_response, indent=4, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
            print("Raw response:", response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    token, query, limit = get_user_input()
    if token and query:
        perform_search(token, query, limit)
