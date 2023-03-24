from flask import Flask, request, send_from_directory, render_template
from sqlalchemy.exc import IntegrityError

from model import Session, Produto
from model.comentario import Comentario

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

from views import *

if __name__ == '__main__':
    app.run(debug=True)