from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_perpustakaan_mhs"
)

def execute_query(sql, data=None):
    cursor = mydb.cursor()

    if data:
        cursor.execute(sql, data)
    else:
        cursor.execute(sql)

    mydb.commit()
    return cursor.rowcount


@app.route('/add', methods=['POST'])
def add():
    id_buku = request.form['id_buku']
    judul_buku = request.form['judul_buku']
    pengarang = request.form['pengarang']
    genre_buku = request.form['genre_buku']
    tanggal_terbit = request.form['tanggal_terbit']

    sql = "INSERT INTO data_buku (id_buku, judul_buku, pengarang, genre_buku, tanggal_terbit) VALUES (%s, %s, %s, %s, %s)"
    data = (id_buku, judul_buku, pengarang, genre_buku, tanggal_terbit)

    row_count = execute_query(sql, data)

    respond = jsonify('Data Berhasil Tersimpan!') if row_count == 1 else jsonify('Data Gagal Tersimpan!')
    respond.status_code = 200 if row_count == 1 else 500

    return respond

@app.route('/edit', methods=['PUT'])
def edit():
    id_buku = request.form['id_buku']
    judul_buku = request.form['judul_buku']
    pengarang = request.form['pengarang']
    genre_buku = request.form['genre_buku']
    tanggal_terbit = request.form['tanggal_terbit']

    sql = "UPDATE data_buku SET id_buku = %s, judul_buku = %s, pengarang = %s, genre_buku = %s, tanggal_terbit = %s WHERE id_buku = %s"
    data = (id_buku, judul_buku, pengarang, genre_buku, tanggal_terbit)

    row_count = execute_query(sql, data)

    respond = jsonify("Data Berhasil Diubah!") if row_count == 1 else jsonify("Data Gagal Diubah!")
    respond.status_code = 200 if row_count == 1 else 500

    return respond

@app.route('/delete', methods=['DELETE'])
def delete():
    id_buku = request.args.get("id_buku")

    row_count = execute_query("DELETE FROM data_buku WHERE id_buku = %s", (id_buku,))

    respond = jsonify('Data Berhasil Dihapus!') if row_count == 1 else jsonify('Data Gagal Dihapus!')
    respond.status_code = 200 if row_count == 1 else 500

    return respond

@app.route('/showdata', methods=['GET'])
def showdata():
    id_buku = request.args.get("id_buku")

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM data_buku WHERE id_buku = %s", (id_buku,))
    book = cursor.fetchone()

    respond = jsonify(book) if book else jsonify('Data tidak ditemukan!')
    respond.status_code = 200 if book else 404

    return respond

@app.route('/showall', methods=['GET'])
def showall():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM data_buku")
    all_books = cursor.fetchall()

    respond = jsonify(all_books) if all_books else jsonify('Data tidak ditemukan!')
    respond.status_code = 200 if all_books else 404

    return respond

if __name__ == "__main__":
    app.run(debug=True)
