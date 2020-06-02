from tornado.httpserver import HTTPServer
from tornado import ioloop
from tornado.wsgi import WSGIContainer
from tornado.log import app_log
import click
import logging
import importlib.util

def make_app(command, server_name, debug):

    app_py_path = command

    print("Fetching Plotly Dash script {}".format(app_py_path))

    spec = importlib.util.spec_from_file_location("userscript", app_py_path)
    userscript = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(userscript)

    app = getattr(userscript, server_name)

    return WSGIContainer(app.server)


@click.command()
@click.option('--port', default=8888, type=click.INT, help='port for the proxy server to listen on')
@click.option('--ip', default=None, help='Address to listen on')
@click.option('--server-name', default='app', type=click.STRING, 
                help='Name of the flask app inside your script (default "app")')
@click.option('--debug/--no-debug', default=False, help='To display debug level logs')
@click.argument('command', nargs=1, required=True)
def run(port, ip, server_name, debug, command):

    if debug:
        app_log.setLevel(logging.DEBUG)
        print('Setting debug')

    app = make_app(command, server_name, debug)

    http_server = HTTPServer(app)

    http_server.listen(port, ip)

    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    run()
