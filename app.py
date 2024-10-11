from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import shutil
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_DIR = 'data'
BACKUP_DIR = 'data_bkp'

def backup_data():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    for file_name in os.listdir(DATA_DIR):
        shutil.copy(os.path.join(DATA_DIR, file_name), os.path.join(BACKUP_DIR, file_name))

def read_csv(file_name):
    with open(os.path.join(DATA_DIR, file_name), mode='r') as file:
        reader = csv.reader(file)
        return list(reader)

def write_csv(file_name, data):
    with open(os.path.join(DATA_DIR, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    backup_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Both fields are required!')
            return redirect(url_for('student_login'))
        
        students = read_csv('students.csv')
        for student in students:
            if student[0] == username and student[1] == password:
                return redirect(url_for('student_menu'))
        flash('Invalid credentials')
    return render_template('student_login.html')

@app.route('/librarian_login', methods=['GET', 'POST'])
def librarian_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Both fields are required!')
            return redirect(url_for('librarian_login'))
        
        librarians = read_csv('librarian.csv')
        for librarian in librarians:
            if librarian[0] == username and librarian[1] == password:
                return redirect(url_for('librarian_menu'))
        flash('Invalid credentials')
    return render_template('librarian_login.html')

@app.route('/student_register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Both fields are required!')
            return redirect(url_for('student_register'))
        
        students = read_csv('students.csv')
        students.append([username, password])
        write_csv('students.csv', students)
        return redirect(url_for('student_login'))
    return render_template('student_register.html')

@app.route('/librarian_register', methods=['GET', 'POST'])
def librarian_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Both fields are required!')
            return redirect(url_for('librarian_register'))
        
        librarians = read_csv('librarian.csv')
        librarians.append([username, password])
        write_csv('librarian.csv', librarians)
        return redirect(url_for('librarian_login'))
    return render_template('librarian_register.html')

@app.route('/student_menu')
def student_menu():
    return render_template('student_menu.html')

@app.route('/librarian_menu')
def librarian_menu():
    return render_template('librarian_menu.html')

@app.route('/view_books')
def view_books():
    books = read_csv('books.csv')
    return render_template('view_books.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        if not title or not author:
            flash('Both fields are required!')
            return redirect(url_for('add_book'))
        
        books = read_csv('books.csv')
        books.append([title, author])
        write_csv('books.csv', books)
        return redirect(url_for('view_books'))
    return render_template('add_book.html')

@app.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    books = read_csv('books.csv')
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        if not title or not author:
            flash('Both fields are required!')
            return redirect(url_for('update_book', book_id=book_id))
        
        books[book_id] = [title, author]
        write_csv('books.csv', books)
        return redirect(url_for('view_books'))
    return render_template('update_book.html', book=books[book_id])

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    books = read_csv('books.csv')
    books.pop(book_id)
    write_csv('books.csv', books)
    return redirect(url_for('view_books'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
