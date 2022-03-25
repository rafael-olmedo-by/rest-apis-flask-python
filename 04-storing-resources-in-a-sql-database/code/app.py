from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from book import Welcome, Books, Book

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

books = []

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Welcome, '/')
api.add_resource(Books, '/books')
api.add_resource(Book, '/book/<string:title>')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True) # to show good error messages
