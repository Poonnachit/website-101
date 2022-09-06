import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "mysecretkey"

conn = mysql.connector.connect(
    host="localhost",
    port=8889,
    user="admin04",
    password="admin004",
    database="car_rental"
)
cursor = conn.cursor(dictionary=True)


@app.route("/")
def home():
    sql = "SELECT * FROM user"
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template("index.html", users=data)


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        tel = request.form['tel']
        email = request.form['email']
    sql = "INSERT INTO user (name, tel, email) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, tel, email))
    flash('User Added Successfully')
    conn.commit()
    return redirect(url_for('home'))


@app.route("/del_user/<id>", methods=['GET'])
def del_user(id):
    sql = "DELETE FROM user WHERE user_id = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    flash('User Deleted Successfully')
    return redirect(url_for('home'))


@app.route('/edit_user/<id>', methods=['GET'])
def edit_user(id):
    sql = "SELECT * FROM user WHERE user_id = %s"
    cursor.execute(sql, (id,))
    data = cursor.fetchone()
    return render_template("edit.html", user=data)


@app.route('/update_user/<id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        name = request.form['name']
        tel = request.form['tel']
        email = request.form['email']
    sql = "UPDATE user SET name = %s, tel = %s, email = %s WHERE user_id = %s"
    cursor.execute(sql, (name, tel, email, id))
    flash('User Updated Successfully')
    conn.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
