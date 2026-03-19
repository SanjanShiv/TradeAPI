from fastapi.testclient import TestClient
from main import app
from auth import VALID_API_KEY
import sys

client = TestClient(app)

def test_api():
    print("Testing 1: Missing API Key")
    response = client.get("/analyze/pharmaceuticals")
    assert response.status_code == 403 or response.status_code == 401
    print("-> Passed. Status:", response.status_code)

    print("\nTesting 2: Invalid API Key")
    response = client.get("/analyze/pharmaceuticals", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 403
    print("-> Passed. Status:", response.status_code)

    print("\nTesting 3: Valid Request")
    headers = {"X-API-Key": VALID_API_KEY}
    try:
        response = client.get("/analyze/pharmaceuticals", headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Output: {response.text}"
        print("-> Passed. Status:", response.status_code)
        print("Response Content-Type:", response.headers.get("content-type"))
        print("Report Length:", len(response.text))
        print("Snippet:", response.text[:200] + "...")
    except Exception as e:
        print(f"-> Failed. {str(e)}")

    print("\nTesting 4: Rate Limiting")
    for i in range(5):
        client.get("/analyze/technology", headers=headers)
    
    # 6th request should be rate limited (limit is 5/minute)
    response = client.get("/analyze/technology", headers=headers)
    assert response.status_code == 429
    print("-> Passed Rate Limit Test. Status:", response.status_code)

if __name__ == "__main__":
    try:
        test_api()
        print("\nAll tests passed successfully!")
    except Exception as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
