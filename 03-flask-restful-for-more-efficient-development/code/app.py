from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

books = [
    {
        "title": "Superstring Theory",
        "price": 59.99,
        "authors": [
            {
                "author": "Michael Green",
                "country": "UK"
            },
            {
                "author": "John Schwarz",
                "country": "USA"
            },
            {
                "author": "Edward Witter",
                "country": "USA"
            }
        ]
    }
]

class Welcome(Resource):
    def get(self):
        return {'message': 'welcome to the bookstore'}

class Books(Resource):
    def get(self):
        return {'books': books}

class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('authors',
        type=dict,
        required=True,
        help='this field cannot be left blank!'
    )
    parser.add_argument('price',
        type=float,
        required=True,
        help='this field cannot be left blank!'
    )

    @jwt_required()
    def get(self, title):
        # for book in books:
        #     if book['title'] == title:
        #         return book
        book = next(filter(lambda x: x['title'] == title, books), None)
        return {'message': book}, 200 if book else 404 # not found and the most popular http status code

    def post(self, title):
        # for book in books:
        #     if book['title'] == title:
        #         return {'messsage': 'this book already exists'}
        if next(filter(lambda x: x['title'] == title, books), None):
            return {'messsage': 'this book already exists'}, 400 # already exists

        request_data = Book.parser.parse_args()

        new_book = {
            'title': title,
            'authors': request_data['authors'],
            'price': request_data['price']
        }
        books.append(new_book)
        return new_book, 201 # created status

    def delete(self, title):
        global books
        books = list(filter(lambda x: x['title'] != title, books))
        return {'message': 'this item has been deleted'}

    def put(self, title):
        request_data = Book.parser.parse_args()

        book = next(filter(lambda x: x['title'] == title, books), None)
        if book is None:
            new_book = {
                'title': title,
                'authors': request_data['authors'],
                'price': request_data['price']
            }
            books.append(new_book)
            return new_book
        else:
            book.update(request_data)
        return {'message': 'this book has been updated'}




api.add_resource(Welcome, '/')
api.add_resource(Books, '/books')
api.add_resource(Book, '/book/<string:title>')

app.run(port=5000, debug=True) # to show good error messages
