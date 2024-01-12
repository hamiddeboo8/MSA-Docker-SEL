from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
severID = environ.get('SERVER_ID')

# connect to Database Module
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    author = db.Column(db.String(120), unique=False, nullable=False)

    def json(self):
        return {'id': self.id,'title': self.title, 'author': self.author}

with app.app_context():
    db.create_all()

#create a test route
@app.route('/test', methods=['GET'])
def test():
    return f"Hello from Book Service, server {severID}"


# create a book recoed
@app.route('/books', methods=['POST'])
def create_book_recoed():
    try:
        data = request.get_json()
        new_book = Book(title=data['title'], author=data['author'])
        db.session.add(new_book)
        db.session.commit()
        return make_response(jsonify(new_book.json()), 201)
    except Exception as e:
        # return make_response(jsonify({'message': 'error in creating book recoed'}), 500)
        return make_response(jsonify({'message': str(e)}), 500)

# get all book recoeds
@app.route('/books', methods=['GET'])
def get_books():
    try:
        books = Book.query.all()
        return make_response(jsonify([book.json() for book in books]), 200)
    except:
        return make_response(jsonify({'message': 'error in getting book records'}), 500)

# get a book record by id
@app.route('/books/<int:id>', methods=['GET'])
def get_book_record(id):
    try:
        book = Book.query.filter_by(id=id).first()
        if book:
            return make_response(jsonify(book.json()), 200)
        return make_response(jsonify({'message': 'book record not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error in getting book record'}), 500)

# update a book record
@app.route('/books/<int:id>', methods=['PUT'])
def update_book_record(id):
    try:
        book = Book.query.filter_by(id=id).first()
        if book:
            data = request.get_json()
            book.title = data['title']
            book.author = data['author']
            db.session.commit()
            return make_response(jsonify(book.json()), 200)
        return make_response(jsonify({'message': 'book record not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error in updating book record'}), 500)

# delete a book record
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book_record(id):
    try:
        book = Book.query.filter_by(id=id).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return make_response(jsonify({'message': 'book record deleted'}), 200)
        return make_response(jsonify({'message': 'book record not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error in deleting book record'}), 500)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
