import json
import urllib.request

API_URL = "https://fakestoreapi.com/users"

def fetch_raw_user_data(url: str) -> list:
    print(f"📡 Connecting to API: {url}")
    
    # 1. Create a Request object and inject a Browser-like User-Agent header
    # This prevents the API from blocking us with a 403 Forbidden error
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    
    # 2. Open the connection using our configured request object
    with urllib.request.urlopen(req) as response:
        # Read the raw incoming bytes and decode them into a text string
        raw_text = response.read().decode('utf-8')
        
        # Parse that text string into a native Python list of dictionaries
        return json.loads(raw_text)

if __name__ == "__main__":
    users = fetch_raw_user_data(API_URL)
    
    print(f"✅ Success! Ingested {len(users)} raw user records.")
    
    print("\n🔍 First user sample profile:")
    print(json.dumps(users[0], indent=4))