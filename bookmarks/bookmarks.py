from flask import Flask, jsonify, request, render_template_string
import json
import os
import uuid

app = Flask(__name__)
book_log_file = 'books.json'

# Ensure the JSON file exists
if not os.path.exists(book_log_file):
    with open(book_log_file, 'w') as file:
        json.dump([], file)

@app.route('/')
def books():
    with open(book_log_file, 'r') as file:
        books = json.load(file)
    return render_template_string(open('bookmarks_template.html').read(), books=books)

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    image_url = request.form.get('image_url')
    current_page = request.form.get('current_page', type=int, default=0)
    last_page = request.form.get('last_page', type=int, default=0)

    if title and author and image_url and current_page is not None and last_page is not None:
        with open(book_log_file, 'r+') as file:
            books = json.load(file)
            book_uuid = str(uuid.uuid4())  # Generate a unique identifier for the new book
            books.append({
                'id': book_uuid,
                'title': title, 
                'author': author, 
                'image_url': image_url,
                'current_page': current_page,
                'last_page': last_page
            })
            file.seek(0)
            json.dump(books, file)
    return jsonify(success=True)

@app.route('/delete', methods=['POST'])
def delete_book():
    book_uuid = request.form.get('id')
    if book_uuid:
        with open(book_log_file, 'r+') as file:
            books = json.load(file)
            books = [book for book in books if book.get('id') != book_uuid]
            file.seek(0)
            file.truncate()  
            json.dump(books, file)  
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Book ID not provided")


@app.route('/update', methods=['POST'])
def update_book():
    book_uuid = request.form.get('id')
    current_page = request.form.get('current_page', type=int)
    if book_uuid and current_page is not None:
        with open(book_log_file, 'r+') as file:
            books = json.load(file)
            for book in books:
                if book['id'] == book_uuid:
                    book['current_page'] = current_page
                    break
            else:
                return jsonify(success=False, message="Book not found")
            file.seek(0)
            file.truncate()
            json.dump(books, file)
        return jsonify(success=True)
    return jsonify(success=False, message="Missing data")


if __name__ == '__main__':
    app.run(debug=True)
