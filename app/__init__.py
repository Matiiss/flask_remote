from flask import Flask, render_template, request, url_for, abort, redirect
from autopc import actions_dct
import logging
from werkzeug.serving import make_server
import threading
# from app.help_with_exe import resource_path
# import sys

import os
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

app = Flask(__name__)

# app.logger.disabled = True
# log = logging.getLogger('werkzeug')
# log.disabled = True

ip_address = None


@app.route('/start_session/<pin>')
def start_session(pin):
    logging.info(f'{os.listdir(os.getcwd() + "/app/templates")}')
    with open(os.getcwd() + '/app/static/checker_file.txt') as file:
        data = file.read().strip()
    with open(os.getcwd() + '/app/static/checker_file.txt', 'w') as file:
        file.write('done')
    if data == 'done':
        abort(403)
    elif data == pin:
        global ip_address
        ip_address = request.remote_addr
        return redirect(url_for('home'))
    else:
        return 'Incorrect PIN'


@app.route('/')
@app.route('/home')
def home():
    if request.remote_addr != ip_address:
        abort(403)
    return render_template('home.html', actions=actions)


@app.route('/actions')
def actions():
    if request.remote_addr != ip_address:
        abort(403)
    action = request.args.get('action')
    args = request.args.get('args')
    if action:
        actions_dct[action](args.split(', '))
    return f'{action}({args.split(", ")})'


class ServerThread(threading.Thread):
    def __init__(self, app, host, port, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.srv = make_server(f'{host}', port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()
