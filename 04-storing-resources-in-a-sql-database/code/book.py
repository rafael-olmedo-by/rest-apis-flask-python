import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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
        connection =  sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM books WHERE title=?'
        result = cursor.execute(query, (title,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'book': {'title': row[0], 'authors': row[1], 'price': row[2]}}
        return {'message': 'Book not found'}, 404

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
