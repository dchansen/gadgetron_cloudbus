import requests


server = 'http://localhost:5000'
requests.post(server + '/cloudbus/add_worker', json = {'port': '9003'})


r = requests.get(server + '/cloudbus/workers')

print(r.json())