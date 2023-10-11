from http.server import HTTPServer, CGIHTTPRequestHandler

if __name__ == "__main__":
    http_server = HTTPServer(("localhost", 7979), CGIHTTPRequestHandler)
    http_server.serve_forever()