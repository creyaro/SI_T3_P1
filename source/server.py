from http.server import BaseHTTPRequestHandler, HTTPServer
import hashlib
import urllib.parse
import json
import os

credentials = {
    "level1": {"username": "user", "password": "827ccb0eea8a706c4c34a16891f84e7b"},
    "level2": {"username": "user", "password": "51558b48f53b70e63e6319214f1ff53b"}, 
    "level3": {"username": "7775d498c7c197bcc136ec9ff402a95a", "password": "794c9608409c8430986e8a067d4a2500"},
    "level4": {"username": "21232f297a57a5a743894a0e4a801fc3", "password": "87abf592d10aa5e73f3d8e5628e8e3f5"},
}

class RequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        # Configura el directorio base para los archivos
        base_dir = "login"

        # Redirige "/" al index
        if self.path == "/":
            self.path = "/index.html"
        
        # Crea la ruta completa del archivo solicitado
        file_path = os.path.join(base_dir, self.path[1:])

        # Determina el tipo de contenido basado en la extensión del archivo
        if self.path.endswith(".html"):
            content_type = "text/html"
        elif self.path.endswith(".js"):
            content_type = "application/javascript"
        elif self.path.endswith(".css"):
            content_type = "text/css"
        else:
            # Retorna 404 si la extensión no es permitida
            self.send_error(404, "Archivo no permitido")
            return
        
        # Intenta abrir y servir el archivo solicitado
        try:
            with open(file_path, "rb") as file:
                self._set_headers(content_type)
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, "File not found")


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(post_data)
        data = json.loads(post_data)

        # Extrae los datos del JSON
        username = data.get('username')
        password = data.get('password')
        level = data.get('level', 'level1')

        if username and password and level in credentials:
            hashed_password = hashlib.md5(password.encode()).hexdigest()

            if level != "level1" and level != "level2":
                username = hashlib.md5(username.encode()).hexdigest()
            
            if username == credentials[level]["username"] and hashed_password == credentials[level]["password"]:
                response = {"status": "success", "message": "Login exitoso. ¡Bien hecho!"}
            else:
                response = {"status": "error", "message": "Invalid username or password."}
        else:
            response = {"status": "error", "message": "Invalid parameters."}

        self._set_headers("application/json")
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor corriendo en http://localhost:{port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
