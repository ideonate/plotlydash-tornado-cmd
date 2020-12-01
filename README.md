# plotlydash-tornado-cmd

Command line wrapper to run a named Plotly Dash script inside a Tornado server.

This project is used in [ContainDS Dashboards](https://github.com/ideonate/cdsdashboards), which is a user-friendly 
way to launch Jupyter notebooks as shareable dashboards inside JupyterHub. Also works with Streamlit and other 
visualization frameworks.

## Install and Run

Install using pip.

```
pip install plotlydash-tornado-cmd
```

The file to start is specified on the command line, for example:

```
plotlydash-tornado-cmd ~/Dev/mydashscript.py
```

By default the server will listen on port 8888, importing the Dash app named 'app', or locating the first dash.Dash 
object that it can find otherwise.

To specify a different port, use the --port flag.

To explicitly specify the name of your dash.Dash app, use the --server-name flag.

```
plotlydash-tornado-cmd --server-name=app --port=8888 ~/Dev/mydashscript.py
```

To run directly in python: `python -m plotlydash_tornado_cmd.main <rest of command line>`

## Changelog

- v0.0.6 Change CWD to script's folder, and also add that folder to the Python search path.
