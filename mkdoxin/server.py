#!/usr/bin/env python3

from http.server import HTTPServer, CGIHTTPRequestHandler
from os import chdir as os_chdir
from logger import logger

log = logger(__name__)


def serve(build_dir):
    """ """
    os_chdir(build_dir)
    port = 8000

    server_object = HTTPServer(
        server_address=("", port), RequestHandlerClass=CGIHTTPRequestHandler
    )

    # Start the web server
    log.info(f"Started Server on http://localhost:{port}")
    log.info("-------------------------------------\n")
    server_object.serve_forever()
