import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
r2 = r1.read().decode("utf-8")
conn.close()

inf = json.loads(r2)
print('El identificador del producto es:', inf['results'][0]['id'])
print('El propósito del producto es:', inf['results'][0]['purpose'][0])
print('El producto ha sido fabricado por:', inf['results'][0]['openfda']['manufacturer_name'][0])
