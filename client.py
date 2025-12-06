import httpx

BASE_URL = "http://localhost:5000/"

#ask for token
print("\nRequesting token...")
res = httpx.post(BASE_URL + "generate", data={"user_id": "123"})
token = res.json().get("token")
print("Token:", token)
#checks token
print("\nVerifying token...")
res = httpx.post(BASE_URL + "verify", data={"token": token})
print(res.json())


print("\nRunning protected application...")
res = httpx.post(BASE_URL + "run_app", data={"token": token})
print(res.json())
