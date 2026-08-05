<<<<<<< HEAD
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
    cursor.execute("SELECT COUNT(*) FROM book")
    total_books = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM student")
    total_students = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM issued_books WHERE status='Issued'")
    issued_books = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()
    return render_template(
        "index.html",
        total_books=total_books,
        total_students=total_students,
        issued_books=issued_books,
        books=books
    )
@app.route("/books")
def books():
    search = request.args.get("search")
    if search:
        cursor.execute("""
        SELECT * FROM book
        WHERE book_name LIKE %s
        OR book_author LIKE %s
        OR category LIKE %s
        """,
        (
            "%"+search+"%",
            "%"+search+"%",
            "%"+search+"%"
        ))
    else:
        cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()
    return render_template(
        "books.html",
        books=books
    )

@app.route("/add_book", methods=["POST"])
def add_book():
    name = request.form["book_name"]
    author = request.form["book_author"]
    category = request.form["category"]
    quantity = request.form["quantity"]
    price = request.form["price"]
    cursor.execute("""
    INSERT INTO book
    (book_name,book_author,category,quantity,price)
    VALUES(%s,%s,%s,%s,%s)
    """,
    (
        name,
        author,
        category,
        quantity,
        price
    ))
    con.commit()
    return redirect("/books")

@app.route("/delete_book/<int:id>")
def delete_book(id):
    cursor.execute(
        "DELETE FROM book WHERE book_id=%s",
        (id,)
    )
    con.commit()
    return redirect("/books")

@app.route("/students")
def students():
    search = request.args.get("search")
    if search:
        cursor.execute("""
        SELECT * FROM student
        WHERE name LIKE %s
        OR phone LIKE %s
        """,
        (
            "%"+search+"%",
            "%"+search+"%"
        ))

    else:
        cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    return render_template(
        "students.html",
        students=students
    )


@app.route("/add_student", methods=["POST"])
def add_student():
    name = request.form["name"]
    phone = request.form["phone"]
    cursor.execute("""
    INSERT INTO student(name,phone)
    VALUES(%s,%s)
    """,
    (
        name,
        phone
    ))
    con.commit()
    return redirect("/students")


@app.route("/delete_student/<string:name>")
def delete_student(name):
    cursor.execute(
        "DELETE FROM student WHERE name=%s",
        (name,)
    )
    con.commit()

    return redirect("/students")
@app.route("/issue")
def issue():
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()
    cursor.execute("SELECT * FROM issued_books")
    issued = cursor.fetchall()
    return render_template(
        "issue.html",
        students=students,
        books=books,
        issued=issued
    )

@app.route("/issue_book", methods=["POST"])
def issue_book():
    student = request.form["student_name"]
    book = request.form["book_id"]
    issue_date = request.form["issue_date"]
    return_date = request.form["return_date"]
    cursor.execute("""
    INSERT INTO issued_books
    (student_name,book_id,issue_date,return_date,status)
    VALUES(%s,%s,%s,%s,%s)
    """,
    (
        student,
        book,
        issue_date,
        return_date,
        "Issued"
    ))
    con.commit()
    return redirect("/issue")
@app.route("/return_book/<int:id>")
def return_book(id):
    cursor.execute("""
    UPDATE issued_books
    SET status='Returned'
    WHERE issue_id=%s
    """, (id,))
    con.commit()
    return redirect("/return")
@app.route("/return")
def return_page():
    cursor.execute("""
    SELECT * FROM issued_books
    WHERE status='Issued'
    """)
    issued = cursor.fetchall()
    return render_template("return.html", issued=issued)
if __name__ == "__main__":
    app.run(debug=True)
=======
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
>>>>>>> 5d55e008ec69c1af3b987ce030d9a1d79a16a01d
