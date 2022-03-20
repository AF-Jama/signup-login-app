import requests

URL = " http://127.0.0.1:5000/"

res = requests.get(URL+'signup')

print(res.status_code)