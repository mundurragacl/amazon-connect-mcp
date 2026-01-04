"""Standalone web server for the Layout Visualizer."""

import http.server
import socketserver
import webbrowser
from .visualizer import get_visualizer_html

PORT = 8765


class VisualizerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(get_visualizer_html().encode())
        else:
            self.send_error(404)


def run_visualizer(open_browser: bool = True):
    """Run the layout visualizer web server."""
    with socketserver.TCPServer(("", PORT), VisualizerHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"🎨 Layout Visualizer running at {url}")
        if open_browser:
            webbrowser.open(url)
        httpd.serve_forever()


if __name__ == "__main__":
    run_visualizer()
