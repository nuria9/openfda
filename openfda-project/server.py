import socket
import http.client
import json
import socketserver


socketserver.TCPServer.allow_reuse_address = True

IP = "127.0.0.1"
PORT = 8000

MAX_OPEN_REQUESTS = 5

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
r2 = r1.read().decode("utf-8")
conn.close()

inf = json.loads(r2)

def process_client(clientsocket):

    mensaje_solicitud = str(clientsocket.recv(1024))
    print(mensaje_solicitud)
    type(mensaje_solicitud)


    contenido = """
      <!doctype html>
      <html>
      <body style='background-color: lightpink'>
        <h1>Bienvenido </h1>
        <h2>Elija una opcion</h2>
        
    <br>
        <form 
            <input type="radio" name="opcion" value="Ingrediente activo">Ingrediente activo<br>
            <input type="radio" name="opcion" value="Empresas">Empresas<br>
            <input type="radio" name="opcion" value="Listado de farmacos">Listado de farmacos<br>
            <input type="radio" name="opcion" value="Listado de empresas">Listado de empresas<br>     
            <input type="submit" value= "Enviar">
        
      </body>
      </html>
    """



    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))

    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)
    clientsocket.close()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    socketserver.TCPServer.allow_reuse_address = True






