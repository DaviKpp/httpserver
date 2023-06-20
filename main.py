import os
import platform
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file_list = self.get_file_list()
            file_list_html = self.generate_file_list_html(file_list)
            self.wfile.write(file_list_html.encode())

        elif self.path == '/header':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            headers = self.generate_headers()
            self.wfile.write(headers.encode())

        elif self.path == '/info':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            info = self.generate_server_info()
            self.wfile.write(info.encode())

        elif self.path == '/hello':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            message = 'Hello!'
            self.wfile.write(message.encode())

        else:
            file_path = self.path[1:]  # Remove leading slash
            if os.path.isfile(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
                self.end_headers()

                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'File not found')

    def get_file_list(self):
        current_directory = os.getcwd()
        file_list = os.listdir(current_directory)
        return file_list

    def generate_file_list_html(self, file_list):
        html = '<html><body>'
        for file in file_list:
            html += f'<a href="/{file}">{file}</a><br>'
        html += '</body></html>'
        return html

    def generate_headers(self):
        headers = str(self.headers)
        return headers

    def generate_server_info(self):
        now = datetime.datetime.now()
        user = os.getlogin()
        os_name = platform.system()
        os_version = platform.release()

        info = f'Data: {now}\n'
        info += f'Usuário: {user}\n'
        info += f'Sistema operacional: {os_name} {os_version}\n'
        return info


def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print('Server running on http://localhost:8000')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
