import hashlib
import json
import urllib.request
import urllib.error

API_URL = "https://fakestoreapi.com/users"

def sanitize_user_records(raw_users: list) -> list:
    """
    Applies strict data minimization and pseudonymization filters
    to ensure the dataset aligns with GDPR/CCPA standards.
    """
    sanitized_records = []
    
    for user in raw_users:
        raw_email = str(user.get("email", "")).strip().lower()
        hashed_email = hashlib.sha256(raw_email.encode('utf-8')).hexdigest()
        
        clean_user = {
            "id": user.get("id"),
            "username": user.get("username"),
            "masked_email": hashed_email,
            "region": {
                "city": user.get("address", {}).get("city"),
                "zipcode": user.get("address", {}).get("zipcode")
            }
        }
        
        sanitized_records.append(clean_user)
        
    return sanitized_records

def fetch_raw_user_data(url: str) -> list:
    print(f"📡 Connecting to API: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=10) as response: 
            raw_text = response.read().decode('utf-8')
            return json.loads(raw_text)
            
    except urllib.error.HTTPError as e:
        # Catches server-side errors (4xx, 5xx)
        print(f"❌ API Server Error encountered! Status Code: {e.code}, Reason: {e.reason}")
        return []
        
    except urllib.error.URLError as e:
        # Catches network/routing errors (DNS failure, offline)
        print(f"❌ Network Connectivity Error! Reason: {e.reason}")
        return []
        
    except Exception as e:
        # Catch-all safety net for any other unexpected bugs (e.g., JSON parsing failure)
        print(f"❌ Unexpected application error: {str(e)}")
        return []



    with urllib.request.urlopen(req) as response:
        raw_text = response.read().decode('utf-8')
        return json.loads(raw_text)

if __name__ == "__main__":
    raw_users = fetch_raw_user_data(API_URL)    

    if raw_users:
        print(f"✅ Success! Ingested {len(raw_users)} raw user records.")
        
        clean_users = sanitize_user_records(raw_users)
        print(f"🔒 GDPR Compliance Layer applied. Records scrubbed and pseudonymized.")
        print("\n🔍 Sanitized compliance-ready user sample profile:")
        print(json.dumps(clean_users[0], indent=4))
    else:
        print("❌ Data pipeline ingestion failed.")

    print(f"✅ Success! Ingested {len(clean_users)} raw user records.")
    
    print("\n🔍 First user sample profile:")
    print(json.dumps(clean_users[0], indent=4))