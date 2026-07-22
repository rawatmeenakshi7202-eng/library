from flask import Flask, render_template, request, redirect
import mysql.connector
app = Flask(__name__)
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="library"
)
cursor = con.cursor()
@app.route("/")
def home():
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    cursor.execute("SELECT * FROM issued_books")
    issued = cursor.fetchall()
    return render_template(
        "index.html",
        books=books,
        students=students,
        issued=issued
    )
@app.route("/add_book", methods=["POST"])
def add_book():
    name = request.form["book_name"]
    author = request.form["book_author"]
    category = request.form["category"]
    quantity = request.form["quantity"]
    price = request.form["price"]
    cursor.execute(
        """
        INSERT INTO book
        (book_name, book_author, category, quantity, price)
        VALUES(%s,%s,%s,%s,%s)
        """,
        (name, author, category, quantity, price)
    )
    con.commit()
    return redirect("/")
@app.route("/delete_book/<int:id>")
def delete_book(id):
    cursor.execute(
        "DELETE FROM book WHERE book_id=%s",
        (id,)
    )
    con.commit()
    return redirect("/")
@app.route("/add_student", methods=["POST"])
def add_student():
    name = request.form["name"]
    phone = request.form["phone"]
    cursor.execute(
        "INSERT INTO student(name,phone) VALUES(%s,%s)",
        (name, phone)
    )
    con.commit()
    return redirect("/")
@app.route("/delete_student/<string:name>")
def delete_student(name):
    cursor.execute(
        "DELETE FROM student WHERE name=%s",
        (name,)
    )
    con.commit()
    return redirect("/")
@app.route("/issue_book", methods=["POST"])
def issue_book():
    student = request.form["student_name"]
    book_id = request.form["book_id"]
    issue = request.form["issue_date"]
    ret = request.form["return_date"]
    cursor.execute(
        """
        INSERT INTO issued_books
        (student_name, book_id, issue_date, return_date, status)
        VALUES(%s,%s,%s,%s,%s)
        """,
        (student, book_id, issue, ret, "Issued")
    )
    con.commit()
    return redirect("/")
@app.route("/return_book/<int:id>")
def return_book(id):
    cursor.execute(
        """
        UPDATE issued_books
        SET status='Returned'
        WHERE issue_id=%s
        """,
        (id,)
    )
    con.commit()
    return redirect("/")
@app.route("/books")
def books():
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()
    return render_template(
        "books.html",
        books=books
    )
if __name__ == "__main__":
    app.run(debug=True)
