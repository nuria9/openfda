import socket
import http.client
import json
import Flask


IP = "212.128.255.130"
PORT = 8049
MAX_OPEN_REQUESTS = 5

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json/?search=active_ingredient:", name , None, headers)
r1 = conn.getresponse()
r2 = r1.read().decode("utf-8")
conn.close()

inf = json.loads(r2)

def process_client(clientsocket):

    mensaje_solicitud = clientsocket.recv(1024)


    contenido = """
      <!doctype html>
      <html>
      <body style='background-color: lightgreen'>
        <h1>Hola, estos son los 10 medicamentos!</h2>
      </body>
      </html>
    """
    a = 0
    for elem in inf['results']:
        if elem['openfda'] and a<10:
            a += 1
            print("El medicamento es:", elem['openfda']['generic_name'][0])
            contenido += (elem['openfda']['generic_name'][0] + "</br>")
        else:
            if a <10: continue
            else: break
    contenido += "</body></html>"


    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))

    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)
    clientsocket.close()


try:

    while True:

        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()


        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)

except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")





