from flask import Flask, jsonify, request # Flask is a class and jsonify and request are methods

app = Flask(__name__)

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

@app.route('/') # 'http://127.0.0.1:5000/'
def hello():
    return jsonify({'message': 'welcome to the bookstore'}) # jsonify('always a dictionary')

@app.route('/books')
def get_books():
    return jsonify({'books': books})

@app.route('/book/<string:title>') # 'http://127.0.0.1:5000/book/some_title'
def get_book_by_title(title):
    for book in books:
        if book['title'] == title:
            return jsonify(book)
    return jsonify({'message': 'this book has not been found'})

@app.route('/book/<string:title>', methods=['POST']) # 'GET' method by default
def post_book_by_title(title):
    for book in books:
        if book['title'] == title:
            return jsonify({'messsage': 'this book already exists'})
    request_data = request.get_json() # read data from a json
    new_book = {
        'title': title,
        'price': request_data['price'],
        'authors': request_data['authors']
    }
    books.append(new_book)
    return jsonify(new_book)

@app.route('/book/<string:title>', methods=['DELETE'])
def delete_book_by_title(title):
    for i in range(len(books)):
        if books[i]['title'] == title:
            del books[i]
            return jsonify({'message': 'this book has been deleted'})
    return jsonify({'message': 'this book has not been found'})

@app.route('/book/<string:title>', methods=['PUT'])
def put_book_by_title(title):
    request_data = request.get_json()
    for book in books:
        if book['title'] == title:
            book.update(request_data) # 'update' method for dictionaries
            return jsonify({'message': 'this book has been updated'})
    new_book = {
        'title': title,
        'price': request_data['price'],
        'authors': request_data['authors']
    }
    books.append(new_book)
    return jsonify(new_book)

app.run(port=5000) # we use an specific port
