import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
r2 = r1.read().decode("utf-8")
conn.close()

repos = json.loads(r2)

repo = repos[0]
print("The owner of the first repository is", repo['owner']['login'])
