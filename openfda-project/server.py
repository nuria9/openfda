import http.server
import http.client
import socketserver
import json
import requests

PORT = 8000


socketserver.TCPServer.allow_reuse_address = True


headers = {'User-Agent': 'http-client'}


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
                           <form action = "/searchDrug">
                                 <input type="submit" value = "Buscar por ingediente"></input>
                                 <input type="text" name="active_ingredient" value=""></input>
                                 Limite:<input type="text" name="limit" value =""><br><br></input>
                           </form>
                           <form action = "/searchCompany">
                                 <input type="submit" value = "Buscar empresas"></input>
                                 <input type="text" name="company" value=""></input>
                                 Limite:<input type="text" name="limit" value =""><br><br></input>
                           </form>
                           <form action ="/listDrugs">
                                 <input type="submit" value="Listado de farmacos"></input>
                                 Limite:<input type="text" name="limit" value =""><br><br></input>
                           </form>
                           <form action = "/listCompanies">
                                 <input type="submit" value="Listado de empresas"></input> 
                                 Limite:<input type="text" name="limit" value =""><br><br></input>    
                           </form>
                           <form action ="/listWarnings">
                                <input type ="submit" value ="Advertencias"></input>
                                Limite:<input type="text" name="limit" value =""><br><br></input>
                           </form>
                           <form action ="/">
                                <input type="submit" value="Menu principal"></input>
                           </form>

                       
                       """
        return html

    def do_Ingrediente(self,principioActivo,limit):
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json/?search=active_ingredient:" + principioActivo +"&limit=100", None, headers)
        r1 = conn.getresponse()


        r2 = r1.read().decode("utf-8")
        conn.close()

        inf = json.loads(r2)
        b = []
        contador = 0
        if 'results' in inf:
            for element in inf['results']:
                contador += 1
                if contador <= limit:
                    if element['openfda']:
                        b.append(element['openfda']['generic_name'][0])
                    else:
                        b.append("Medicamento desconocido")
                else:
                    break


        html = """
                       <body align=center style='background-color: lightpink'>
                       <h1> Los medicamentos con el principio activo deseado son: </h1><br><ul>
                       """
        if 'results' in inf:
            for item in b:
                html += "<li>" + item + "</li>"
        else:
            html += "<li>" + "No hay resultados" + "</li>"
        html += """
                       </ul>"""

        return html

    def do_Empresas1(self,empresa,limit):
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
                    d.append("Empresa desconocida")



        html = """
                               <body align=center style='background-color: lightpink'>
                               <h1> Las empresas que contienen su busqueda son: </h1><br><ul>
                               """
        contador = 0
        if 'results' in inf:
            for item in d:
                if item.find(empresa) != -1:
                    contador += 1
                    if contador<= limit:
                        html += "<li>" + item + "</li>"
                    else:
                        break




        else:
            html += "<li>" + "No se han encontrado resultados" + "</li>"

        html += """
                               </ul>"""

        return html

    def do_Empresas2(self,limit):
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?&limit=100", None,
                     headers)
        r1 = conn.getresponse()

        r2 = r1.read().decode("utf-8")
        conn.close()

        inf = json.loads(r2)
        c = []
        contador = 0
        if 'results' in inf:
            for element in inf['results']:
                contador += 1
                if contador <= limit:
                    if element['openfda']:
                        c.append(element['openfda']['manufacturer_name'][0])
                    else:
                        c.append("Empresa desconocida")
                else:
                    break
        html = """
                <body align=center style='background-color: lightpink'>
                <h1> Listado de empresas: </h1><br><ul>
                """
        if 'results' in inf:
            for item in c:
                html += "<li>" + item + "</li>"
        else:
            html += "<li>" + "No se han encontrado resultados" + "</li>"

        html += """
                </ul>"""
        return html

    def listWarnings(self,limit):
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?&limit=100", None, headers)
        r1 = conn.getresponse()

        r2 = r1.read().decode("utf-8")
        conn.close()

        inf = json.loads(r2)
        e = []
        contador = 0
        for element in inf['results']:
            contador += 1
            if contador <= limit:
                print("0")
                try:
                    element['warnings']
                    e.append(element['warnings'][0])
                except KeyError:
                    try:
                        element['warnings_and_cautions']
                        e.append(element['warnings_and_cautions'][0])
                    except KeyError:
                        e.append("Se desconocen las advertencias")
            else:
                break

                #if element['warnings']:
                #    e.append(element['warnings'][0])
                #elif element['warnings_and_cautions']:
                #    e.append(element['warnings_and_cautions'][0])
                #else:
                #    e.append("Se desconocen las advertencias")
        html = """
                        <body align=center style='background-color: lightpink'>
                        <h1> Atencion: </h1><br><ul>
                        """
        for item in e:
            html += "<li>" + item + "</li>"

        html += """
                        </ul>"""
        return html


    def do_Farmacos(self,limit):
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?&limit=100", None, headers)
        r1 = conn.getresponse()
        r2 = r1.read().decode("utf-8")
        conn.close()

        inf = json.loads(r2)
        a = []
        contador = 0
        for element in inf['results']:
            contador += 1
            if contador <= limit:
                if element['openfda']:
                    a.append(element['openfda']['generic_name'][0])
                else:
                    a.append("Se desconoce el nombre del medicamento")
            else:
                break
        html = """
                <body align=center style='background-color: lightpink'>
                <h1> La informacion buscada es: </h1><br><ul>
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
        consulta =""
        opcion = ""
        print(self.path)
        lista_respuesta = self.path.split("?")
        print(lista_respuesta)
        busqueda = lista_respuesta[0]


        if busqueda == "/searchDrug":
            parametros = lista_respuesta[1].split("&")
            opcion = parametros[0].split("=")[1]
            if len(parametros) == 2:
                limite = parametros[1].split("=")[1]
                if limite != "":
                    limit = int(limite)
                else:
                        limit = 1
            else:
                limit = 1
            consulta = self.do_Ingrediente(opcion,limit)
        elif busqueda == "/searchCompany":
            parametros = lista_respuesta[1].split("&")
            opcion = parametros[0].split("=")[1]
            if len(parametros) == 2:
                limite = parametros[1].split("=")[1]
                if limite != "":
                    limit = int(limite)
                else:
                    limit = 1
            else:
                limit = 1
            consulta = self.do_Empresas1(opcion,limit)
        elif busqueda == "/listCompanies":
            limite = lista_respuesta[1].split("=")[1]
            if limite != "":
                limit = int(limite)
            else:
                limit = 1
            consulta = self.do_Empresas2(limit)
        elif busqueda == "/listDrugs":
            limite = lista_respuesta[1].split("=")[1]
            if limite != "":
                limit = int(limite)
            else:
                limit = 1
            consulta = self.do_Farmacos(limit)
        elif busqueda == "/listWarnings":
            limite = lista_respuesta[1].split("=")[1]
            if limite != "":
                limit = int(limite)
            else:
                limit = 1
            consulta = self.listWarnings(limit)
        elif busqueda =="/":
            consulta = self.paginaPrincipal()
      
        elif busqueda == "/redirect":
            path = "/"
            self.send_response(302)
            new_path ='%s%s'%('http://127.0.0.1:8000',path)
            self.send_header('Location',new_path)
            self.end_headers()
        else:
            self.send_response(404)

            consulta = """
            <html>
                <body align=center style='background-color: lightpink'>
                <h1>ERROR 404 </h1>
                <h2>El recurso solicitado no se encuentra en el servidor</h2>
                
             """



        message = consulta + "</body></html>"
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
