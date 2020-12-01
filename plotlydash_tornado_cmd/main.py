import os
import logging
import importlib.util
import sys

from tornado.httpserver import HTTPServer
from tornado import ioloop
from tornado.wsgi import WSGIContainer
from tornado.log import app_log
import click

class DashException(Exception):
    pass

def make_app(command, server_name=None, debug=False):

    # Command can be absolute, or could be relative to cwd
    app_py_path = os.path.join(os.getcwd(), command)

    print("Fetching Plotly Dash script {}".format(app_py_path))

    dirname = os.path.dirname(app_py_path)

    basename = os.path.basename(app_py_path)

    (scriptname, _) = os.path.splitext(basename)

    if os.path.isdir(dirname):
        print("CWD to {}".format(dirname))
        os.chdir(dirname)

        # Add script's folder to Python search path too
        sys.path.append(dirname)

    print("Importing user Dash app")

    spec = importlib.util.spec_from_file_location(scriptname, app_py_path)
    userscript = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(userscript)

    app = None

    if server_name is not None:
        # We have been given an explicit server name (e.g. 'app')
        app = getattr(userscript, server_name, None)

    else:
        # Look for 'app' first, but if it's not right just search for the first dash.Dash object
        
        app = getattr(userscript, 'app', None)

        dashclassstr = "dash.Dash'>"

        if app is None or not dashclassstr in str(type(app)):
            from inspect import getmembers
            membs = getmembers(userscript, lambda x: dashclassstr in str(type(x)))
            if len(membs) > 0:
                app = membs[0][1]

    if app is None:
        raise DashException('Cannot find a Dash app inside your script file. There needs to be a dash.Dash object. Looking for an object based on server_name {}.'.format(server_name))

    return WSGIContainer(app.server)


@click.command()
@click.option('--port', default=8888, type=click.INT, help='port for the proxy server to listen on')
@click.option('--ip', default=None, help='Address to listen on')
@click.option('--server-name', default=None, type=click.STRING, 
                help='Name of the flask app inside your script (default None means search for a suitable dash.Dash var)')
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

    try:

        run()

    except SystemExit as se:
        print('Caught SystemExit {}'.format(se))
