import requests
import json

results = requests.post("http://localhost:8081/player", data={"position": 3}).json()
print(results)

# results = requests.delete("http://localhost:8081/player/-LzE6Hqw3321Go9Kp0cX")
# print(results)

# results = requests.patch("http://localhost:8081/player/-LzEJAw2l8C9L3hvj-Me").json()
# print(results)

# results = requests.get("http://localhost:8081/player").json()
# print(json.dumps(results, indent=2))

# results = requests.patch("http://localhost:8081/player/-LzEJAw2l8C9L3hvj-Me").json()
# print(results)