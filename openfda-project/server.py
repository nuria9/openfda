import socket
import http.client
import json
import socketserver



IP = "212.128.254.150"
PORT = 8080
MAX_OPEN_REQUESTS = 5

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
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
        <h1>Bienvenido elija una opción</h2>
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

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketserver.TCPServer.allow_reuse_address = True


try:
    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUESTS)
    while True:

        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()


        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)

except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")





