"""
stub_http
~~~~~~~~~

A stubbed HTTP server for testing articleone.http.
"""
import logging

from flask import abort, Flask, request


# Silence the logger since this is just for test cases.
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Create the web application.
app = Flask(__name__)


# Utility functions.
def shutdown_server():
    """Shutdown the server."""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# Responders.
@app.route('/401', methods=['GET',])
def error_401():
    """Respond to the 401 error test."""
    return ('Unauthorized', 401)


@app.route('/404', methods=['GET',])
def error_404():
    """Respond to the 404 error test."""
    return ('Unauthorized', 404)


@app.route('/500', methods=['GET',])
def error_500():
    """Respond to the 500 error test."""
    return ('Internal server error', 500)


@app.route('/get', methods=['GET',])
def get():
    """Respond to the http.get test."""
    head = {'Content-Type': 'text/plain; charset=utf-8',}
    body = 'success'
    return (body, head)


@app.route('/shutdown', methods=['GET',])
def shutdown():
    """Process request to shutdown the server."""
    shutdown_server()
    return 'Shutting down'


# Mainline.
if __name__ == '__main__':
    app.run(debug=True)