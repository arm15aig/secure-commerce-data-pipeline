import hashlib
import json
import os
import boto3
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

def lambda_handler(event, context):
    print("Cloud execution triggered via AWS EventBridge Scheduler.")

    try:
        raw_users = fetch_raw_user_data(API_URL)
        if not raw_users:
            raise RuntimeError("Pipeline stopped: No records recovered from the target API.")
            
        clean_users = sanitize_user_records(raw_users)

        bucket_name = os.environ.get('BUCKET_NAME')
        if not bucket_name:
            raise ValueError("Critical Configuration Error: BUCKET_NAME environment variable is missing!")
        
        s3_client = boto3.client('s3')
        file_key = "ingested-data/sanitized_users_batch.json"
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(clean_users, indent=4),
            ContentType='application/json'
        )
        
        print(f"🎉 Success! Securely uploaded batch data to S3 Data Lake: s3://{bucket_name}/{file_key}")
        return {"statusCode": 200, "body": "Data ingestion complete."}
    
    except Exception as e:
        print(f"❌ Critical Pipeline Failure: {str(e)}")
        raise e

if __name__ == "__main__":
    print("Running pipeline in local development mode...")
    raw_users = fetch_raw_user_data(API_URL)    

    if raw_users:
        print(f"✅ Success! Ingested {len(raw_users)} raw user records.")
        clean_users = sanitize_user_records(raw_users)
        print(f"🔒 GDPR Compliance Layer applied. Records scrubbed and pseudonymized.")

        os.makedirs('data', exist_ok=True)
        with open('data/sanitized_users.json', 'w') as f:
            json.dump(clean_users, f, indent=4)
            
        print("💾 Progress saved locally to data/sanitized_users.json")
        print("\n🔍 Sanitized compliance-ready user sample profile:")
        print(json.dumps(clean_users[0], indent=4))
    else:
        print("❌ Local data pipeline ingestion failed.")
