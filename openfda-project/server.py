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
                                 </input>
                                 <input type="radio" name="opcion" value="Empresas1">Empresas
                                 </input>
                                 <input type="radio" name="opcion" value="Farmacos">Listado de farmacos
                                 </input>
                                 <input type="radio" name="opcion" value="Empresas2">Listado de empresas<br><br>
                                 </input>     
                                 <input type=text name ="ingr" value= "activo"><br><br>
                                 </input>
                                 <input type="submit" value= "Enviar">
                                 </input>
                                 
                           </form>

                       
                       """
        return html

    def do_Ingrediente(self,principioActivo):
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json/?search=active_ingredient:" + principioActivo +"&limit=100", None, headers)
        r1 = conn.getresponse()

        r2 = r1.read().decode("utf-8")
        conn.close()

        inf = json.loads(r2)
        b = []
        for element in inf['results']:
            if element['openfda']:
                b.append(element['openfda']['substance_name'][0])
            else:
                continue
        html = """
                       <h1> Los medicamentos con el principio activo deseado son: </h1><br>
                       """
        for item in b:
            html += "<li>" + item + "</li>"
        html += """
                       </ul>"""

        return html

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
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?&limit=100", None,
                     headers)
        r1 = conn.getresponse()

        r2 = r1.read().decode("utf-8")
        conn.close()

        inf = json.loads(r2)
        c = []
        for element in inf['results']:
            if element['openfda']:
                c.append(element['openfda']['manufacturer_name'][0])
            else:
                c.append("Desconocida")
        html = """
                <h1> Listado de empresas: </h1><br>
                """
        for item in c:
            html += "<li>" + item + "</li>"
        html += """
                </ul>"""

        return html

    def do_Farmacos(self):
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?&limit=100", None, headers)
        r1 = conn.getresponse()

        r2 = r1.read().decode("utf-8")
        conn.close()

        inf = json.loads(r2)
        a = []
        for element in inf['results']:
            if element['openfda']:
                a.append(element['openfda']['substance_name'][0])
            else:
                continue
        html = """
                <h1> La informacion buscada es: </h1><br>
                """
        for item in a:
            html += "<li>" + item + "</li>"
        html += """
                </ul>"""

        return html
            



    def do_GET(self):
        consulta =""
        opcion = "principal"
        lista_respuesta = self.path.split("?")
        print(lista_respuesta)
        if len(lista_respuesta) > 1:
            parametros = lista_respuesta[1].split("&")
            opcion = parametros[0].split("=")[1]
            ingrediente = parametros[1].split("=")[1]
            print("opcion: ", opcion)
            print("ingrediente: ", ingrediente)
        else:
            parametros = ""


        if opcion == "Ingrediente":
            consulta = self.do_Ingrediente(ingrediente)
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
