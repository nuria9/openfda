import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json/?search=active_ingredient:acetylsalicylic&limit=100", None, headers)
r1 = conn.getresponse()

r2 = r1.read().decode("utf-8")
conn.close()

inf = json.loads(r2)

for element in inf['results']:
    print("El id del producto es:", element['id'])
    if element['openfda']:
        print("  El fabricante es:" , element['openfda']['manufacturer_name'][0],"\n")
    else:
        print("  Fabricante desconocido\n")
