import http.server
import http.client
import socketserver
import json

PORT = 8000
INDEX_FILE = "index.html"
socketserver.TCPServer.allow_reuse_address = True


NOMBRE_APIREST = "api.fda.gov"
DIR_APIREST = "/drug/label.json"
headers = {'User-Agent': 'http-client'}

CERRAR = "</body></html>"

class ManejaRequest(http.server.BaseHTTPRequestHandler):


    def paginaPrincipal (self):
        html = """
                   <html>
                       <head>
                           <title>Bienvenido!!</title>
                       </head>
                       <body align=center style='background-color: lightpink'>
                           <h1>Elija una opcion </h1>
                           <br>
                           <form> 
                                 <input type="radio" name="opcion" value="Ingrediente" checked>Ingrediente activo
                                 <input type=text value= "Introduca ingrediente activo"><br>
                                 </input>
                                 <input type="radio" name="opcion" value="Empresas1">Empresas<br>
                                 </input>
                                 <input type="radio" name="opcion" value="Farmacos">Listado de farmacos<br>
                                 </input>
                                 <input type="radio" name="opcion" value="Empresas2">Listado de empresas<br>
                                 </input>     
                                 <input type="submit" value= "Enviar">
                                 </input>
                           </form>

                       
                       """
        return html

    def do_Ingrediente(self):
        html = """
            <<ul> 
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            </ul> """

    def do_Empresas1(self):
        html = """
            <ul> 
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            </ul> """

        return html

    def do_Empresas2(self):
        html = """
            <ul> 
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            </ul> """
        return html

    def do_Farmacos(self):
        html = """
            <ul> 
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1
            hola farmaco1 
            </ul> """
        return html
            
        



    def do_GET(self):
        opcion = "principal"
        lista_respuesta = self.path.split("?")
        print(lista_respuesta)
        if len(lista_respuesta) > 1:
            parametros = lista_respuesta[1].split("=")
            nombre, valor = parametros[0], parametros[1]
            opcion = parametros[1]
            print(nombre, ' y ', valor)

        else:
            parametros = ""


        if opcion == "Ingrediente":
            consulta = self.do_Ingrediente()
        elif opcion == "Empresas1":
            consulta = self.do_Empresas1()
        elif opcion == "Empresas2":
            consulta = self.do_Empresas2()
        elif opcion == "Farmacos":
            consulta = self.do_Farmacos()
        else:
            consulta = ""

        message = self.paginaPrincipal() + consulta + "</body></html>"
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes(message, "utf8"))


#------------------------------------#

socketserver.TCPServer.allow_reuse_address = True
# Handler = http.server.SimpleHTTPRequestHandler
Handler = ManejaRequest
# es una instancia de una clase q se encarga de responde a las peticciones http que puede venir de dos sitios, un ordenador o el test de la practica

httpd = socketserver.TCPServer(("", PORT), Handler)
print("Sirviendo en el puerto:", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("El usuario ha interrumpido el servidor en el puerto:", PORT)
    print("Reanudelo de nuevo")

print("Servidor parado")
