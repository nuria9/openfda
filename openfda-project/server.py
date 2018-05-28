import http.server
import http.client
import socketserver
import json
import requests

PORT = 8000

socketserver.TCPServer.allow_reuse_address = True

NOMBRE_APIREST = "api.fda.gov"
DIR_APIREST = "/drug/label.json"
headers = {'User-Agent': 'http-client'}

CERRAR = "</body></html>"


class ManejaRequest(http.server.BaseHTTPRequestHandler):

    def paginaPrincipal(self):
        html = """
                   <html>
                       <head>
                           <title>Bienvenido!!</title>
                       </head>
                       <body align=center style='background-color: lightpink'>
                           <h1>Elija una opcion </h1>
                           <br>
                           <form action = "/searchDrug">
                                 <input type="submit" value = "Buscar por ingediente"></input>
                                 <input type="text" name="active_ingredient" value=""><br><br></input>
                           </form>
                           <form action = "/searchCompany">
                                 <input type="submit" value = "Buscar empresas"></input>
                                 <input type="text" name="company" value=""></input>
                           </form>
                           <form action ="/listDrugs">
                                 <input type="submit" value="Listado de farmacos"></input>
                           </form>
                           <form action = "/listCompanies">
                                 <input type="submit" value="Listado de empresas"></input>     
                           </form>
                           <form action ="/">
                                <input type="submit" value="Menu principal"></input>

                       """
        return html

    def do_Ingrediente(self, principioActivo):
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json/?search=active_ingredient:" + principioActivo + "&limit=100", None,
                     headers)
        r1 = conn.getresponse()

        r2 = r1.read().decode("utf-8")
        conn.close()

        inf = json.loads(r2)
        b = []
        if 'results' in inf:
            for element in inf['results']:
                if element['openfda']:
                    b.append(element['openfda']['substance_name'][0])
                else:
                    continue

        html = """
                       <h1> Los medicamentos con el principio activo deseado son: </h1><br>
                       """
        if 'results' in inf:
            for item in b:
                html += "<li>" + item + "</li>"
        else:
            html += "<li>" + "No hay resultados" + "</li>"
        html += """
                       </ul>"""

        return html

    def do_Empresas1(self, empresa):
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?&limit=100", None,
                     headers)
        r1 = conn.getresponse()

        r2 = r1.read().decode("utf-8")
        conn.close()

        inf = json.loads(r2)
        d = []
        if 'results' in inf:
            for element in inf['results']:
                if element['openfda']:
                    d.append(element['openfda']['manufacturer_name'][0])

                else:
                    continue
        html = """
                               <h1> Las empresas que contienen su busqueda son: </h1><br>
                               """
        if 'results' in inf:
            for item in d:
                if item.find(empresa) != -1:
                    html += "<li>" + item + "</li>"
        else:
            html += "<li>" + "No se han encontrado resultados" + "</li>"

        html += """
                               </ul>"""

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
                a.append(element['openfda']['generic_name'][0])
            else:
                continue
        html = """
                <h1> La informacion buscada es: </h1><br>
                """
        if 'results' in inf:
            for item in a:
                html += "<li>" + item + "</li>"
        else:
            html += "<li>" + "No hay resultados" + "</li>"

        html += """
                </ul>"""

        return html

    def do_GET(self):
        consulta = ""
        opcion = ""
        lista_respuesta = self.path.split("?")
        print(lista_respuesta)
        busqueda = lista_respuesta[0]
        print("La busqueda es: ",busqueda)

        if busqueda == "/searchDrug":
            parametros = lista_respuesta[1].split("=")
            opcion = parametros[1]
            consulta = self.do_Ingrediente(opcion)
        elif busqueda == "/searchCompany":
            parametros = lista_respuesta[1].split("=")
            opcion = parametros[1]
            consulta = self.do_Empresas1(opcion)
        elif busqueda == "/listCompanies":
            consulta = self.do_Empresas2()
        elif busqueda == "/listDrugs":
            consulta = self.do_Farmacos()
        else:
            consulta = ""

        message = self.paginaPrincipal() + consulta + "</body></html>"
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes(message, "utf8"))


# ------------------------------------#

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
