import os
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler


class AJHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_PUT(self):
        path: str = self.translate_path(self.path)
        print(f"path is {path}")
        if path.endswith("/"):
            self.send_response(405, "Method Not Allowed")
            self.wfile.write("PUT not allowed on a directory\n".encode())
        else:
            try:
                os.makedirs(os.path.dirname(path))
            except FileExistsError:
                pass
            length = int(self.headers["Content-Length"])
            print(f"length is {length}")
            with open(path, "wb") as f:
                f.write(self.rfile.read(length))
            self.send_response(201, "Created")


def run(handler_class=AJHTTPRequestHandler, server_class=HTTPServer):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        keyfile="./key.pem",
        certfile="./cert.pem",
        server_side=True
    )
    print("Server started at port 127.0.0.1:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
